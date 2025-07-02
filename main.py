# main.py – fix de coroutine + domínio ngrok estático + GerarItens
"""Bootstrap do servidor FastAPI + ngrok.

Fluxo:
1. Recebe webhook (webhook.processar_webhook_completo);
2. Se NÃO houver sub‑formulários → chama GerarItens e encerra;
3. Caso contrário → cria checklist via POST.ChecklistCreator.

Mantém domínio ngrok fixo em https://enormous-infinite-tahr.ngrok-free.app.
"""

from __future__ import annotations

import asyncio
import inspect
import nest_asyncio
from pyngrok import ngrok, conf
import uvicorn
import os
import json
from datetime import datetime
from typing import Any, Dict

# ──────────────────────────────────────────────────────────────
# Módulos internos do projeto
# ──────────────────────────────────────────────────────────────
import webhook  # contém FastAPI + processar_webhook_completo
import GET      # cacheado nos side‑effects
from POST import ChecklistCreator  # criador de checklists

# ──────────────────────────────────────────────────────────────
# Função alternativa quando não houver itens habilitados
# ──────────────────────────────────────────────────────────────

def GerarItens(payload: Dict[str, Any]) -> None:
    """Rotina chamada quando o webhook não traz sub‑formulários."""
    print("[GerarItens] Nenhum item habilitado recebido. Executando rotina...")
    ts = datetime.now().isoformat(timespec="seconds").replace(":", "-")
    path = f"webhooks_sem_itens/{ts}.json"
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fp:
        json.dump(payload, fp, ensure_ascii=False, indent=2)
    print(f"[GerarItens] Payload salvo em {path}")

# ──────────────────────────────────────────────────────────────
# Monkey‑patch em webhook.processar_webhook_completo
# ──────────────────────────────────────────────────────────────

_original_processar = webhook.processar_webhook_completo


def _processar_webhook_wrapper(*args, **kwargs):
    """Encaixa decisão GerarItens vs criar checklist.

    Sempre devolve **dict** (nunca coroutine) para evitar problemas
    no jsonable_encoder do FastAPI.
    """
    # Chama função original (sincrona ou async)
    if inspect.iscoroutinefunction(_original_processar):
        resultado = asyncio.run(_original_processar(*args, **kwargs))
    else:
        resultado = _original_processar(*args, **kwargs)

    total = resultado.get("total_itens_habilitados", 0)
    print(f"[Wrapper] total_itens_habilitados = {total}")

    if total == 0:
        GerarItens(resultado)
        resultado.setdefault("status", "OK")
        resultado["acao_executada"] = "GerarItens"
        return resultado

    # Há itens – cria checklist
    try:
        checklist_id = ChecklistCreator.criar_checklist_completo(
            identificacao=resultado["identificacao"],
            itens_por_tipo=resultado["itens_por_tipo"],
        )
        resultado["checklist_id"] = checklist_id
        resultado.setdefault("status", "OK")
        resultado["acao_executada"] = "POST_Checklist"
    except Exception as exc:
        print(f"[Wrapper] Erro ao criar checklist: {exc}")
        resultado["status"] = "ERRO"
        resultado["erro"] = str(exc)
    return resultado

# Aplica monkey‑patch
webhook.processar_webhook_completo = _processar_webhook_wrapper  # type: ignore[attr-defined]

# ──────────────────────────────────────────────────────────────
# Bootstrap FastAPI + ngrok
# ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    nest_asyncio.apply()

    RESERVED_DOMAIN = "enormous-infinite-tahr.ngrok-free.app"

    # Token do ngrok (opcional, mas necessário p/ túnel público)
    auth_token = "2yy04GbRMzDFhGgaRo3PGRqV5tC_4gkaL24YZ3yhDkNq9wDuh"
    if auth_token:
        conf.get_default().auth_token = auth_token
        try:
            public_url = ngrok.connect(8000, domain=RESERVED_DOMAIN).public_url  # type: ignore[arg-type]
        except Exception as exc:
            print(f"[main] ⚠️  Falha ao usar domínio reservado: {exc}. Criando túnel dinâmico…")
            public_url = ngrok.connect(8000).public_url  # type: ignore[arg-type]
    else:
        print("[main] ⚠️  NGROK_AUTH_TOKEN não definido — iniciando sem túnel.")
        public_url = f"https://{RESERVED_DOMAIN} (offline)"

    print(f"[main] 🔗 URL público: {public_url}")

    # Instância FastAPI
    if hasattr(webhook, "criar_app_fastapi"):
        fastapi_app = webhook.criar_app_fastapi()  # type: ignore[attr-defined]
    else:
        fastapi_app = getattr(webhook, "app")  # fallback para webhook.app

    print("[main] 🚀 Servidor FastAPI em http://localhost:8000 …")
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8000, reload=False)
