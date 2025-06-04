# main.py - Arquivo principal que orquestra o sistema completo

# Instalar dependências se necessário:
# pip install fastapi nest-asyncio pyngrok uvicorn

import nest_asyncio
from pyngrok import ngrok, conf
import uvicorn
import sys
import os

# Importar módulos do projeto
import webhook
import GET


def verificar_dependencias():
    """
    Verifica se todas as dependências estão instaladas
    """
    dependencias = ['fastapi', 'pyngrok', 'uvicorn', 'requests']
    faltando = []

    for dep in dependencias:
        try:
            __import__(dep)
        except ImportError:
            faltando.append(dep)

    if faltando:
        print("❌ Dependências faltando:")
        for dep in faltando:
            print(f"   - {dep}")
        print("\n💡 Instale com: pip install " + " ".join(faltando))
        return False

    return True


def configurar_ngrok():
    """
    Configura o ngrok com o token de autenticação
    """
    try:
        # Configurar authtoken (substitua pelo seu real)
        auth_token = "2xx8LQUnhKIsNUxERL0JGniq3xg_3ahxzWJjMc7K1kduj1xnm"
        conf.get_default().auth_token = auth_token

        print("✅ ngrok configurado com sucesso!")
        return True

    except Exception as e:
        print(f"❌ Erro ao configurar ngrok: {e}")
        return False


def inicializar_sistema():
    """
    Inicializa o sistema completo
    """
    print("🚀 INICIANDO SISTEMA DE WEBHOOK E FORMULÁRIOS")
    print("=" * 60)

    # Verificar dependências
    print("📦 Verificando dependências...")
    if not verificar_dependencias():
        return False

    # Aplicar correção para loop de eventos
    nest_asyncio.apply()
    print("🔧 Loop de eventos configurado.")

    # Configurar ngrok
    print("🌐 Configurando ngrok...")
    if not configurar_ngrok():
        return False

    print("✅ Sistema inicializado com sucesso!")
    return True


def criar_tunel_ngrok(porta=8000):
    """
    Cria o túnel ngrok
    """
    try:
        public_url = ngrok.connect(porta)
        print(f"🔗 Túnel ngrok criado: {public_url}")
        return public_url
    except Exception as e:
        print(f"❌ Erro ao criar túnel ngrok: {e}")
        return None


def exibir_informacoes_sistema(public_url):
    """
    Exibe informações do sistema para o usuário
    """
    print("\n" + "=" * 60)
    print("🎯 SISTEMA PRONTO PARA USO!")
    print("=" * 60)

    print(f"🔗 URL pública do webhook: {public_url}/webhook")
    print(f"📋 Modo de operação: 🔄 Cache atualizado a cada webhook")

    print("\n🌐 ENDPOINTS DISPONÍVEIS:")
    print(f"   POST {public_url}/webhook")
    print("      └── Receber webhooks (atualiza cache automaticamente)")

    print(f"   GET  {public_url}/itens-habilitados")
    print("      └── Listar itens do último webhook processado")

    print(f"   GET  {public_url}/recarregar-cache")
    print("      └── Forçar recarregamento manual do cache")

    print(f"   GET  {public_url}/status-cache")
    print("      └── Verificar status e informações do cache")

    print("\n📁 ARQUIVOS DO PROJETO:")
    print("   📄 main.py - Orquestrador principal (este arquivo)")
    print("   📄 webhook.py - Funções de processamento do webhook")
    print("   📄 GET.py - Funções de requisição e cache de formulários")

    print("\n🔄 FLUXO DE OPERAÇÃO:")
    print("   1. Webhook recebido → Atualiza cache de formulários")
    print("   2. Extrai informações do webhook → Identifica itens habilitados")
    print("   3. Busca formulários no cache → Processa resultados")
    print("   4. Salva resultados por tipo → Retorna resposta")

    print("\n💡 DICAS DE USO:")
    print("   • O cache é atualizado automaticamente a cada webhook")
    print("   • Resultados são salvos em arquivos JSON por tipo (FT, FA, FO, GC, VC)")
    print("   • Use /status-cache para monitorar o sistema")
    print("   • Logs detalhados são exibidos no console")


def testar_modulos():
    """
    Testa se os módulos estão funcionando corretamente
    """
    print("\n🧪 Testando módulos...")

    try:
        # Testar GET.py
        buscador = GET.FormulariosBuscador()
        print("✅ GET.py: Módulo carregado corretamente")

        # Testar webhook.py
        app = webhook.criar_app_fastapi()
        print("✅ webhook.py: Módulo carregado corretamente")

        print("✅ Todos os módulos funcionando!")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar módulos: {e}")
        return False


def main():
    """
    Função principal do sistema
    """
    try:
        # Inicializar sistema
        if not inicializar_sistema():
            print("❌ Falha na inicialização do sistema.")
            sys.exit(1)

        # Testar módulos
        if not testar_modulos():
            print("❌ Falha nos testes dos módulos.")
            sys.exit(1)

        # Criar aplicação FastAPI usando as funções do webhook
        print("\n🏗️  Criando aplicação FastAPI...")
        app = webhook.criar_app_fastapi()

        # Criar túnel ngrok
        print("🌐 Criando túnel ngrok...")
        public_url = criar_tunel_ngrok(8000)

        if not public_url:
            print("❌ Falha ao criar túnel ngrok.")
            sys.exit(1)

        # Exibir informações do sistema
        exibir_informacoes_sistema(public_url)

        # Iniciar servidor
        print("\n🚀 INICIANDO SERVIDOR...")
        print("   (Pressione Ctrl+C para parar)")
        print("-" * 60)

        uvicorn.run(app, host="0.0.0.0", port=8000)

    except KeyboardInterrupt:
        print("\n\n⏹️  Sistema interrompido pelo usuário.")
        print("👋 Encerrando graciosamente...")

    except Exception as e:
        print(f"\n❌ Erro inesperado: {e}")
        sys.exit(1)

    finally:
        # Cleanup se necessário
        print("🧹 Limpeza finalizada.")


def executar_teste_rapido():
    """
    Executa um teste rápido do sistema sem iniciar o servidor
    """
    print("🧪 TESTE RÁPIDO DO SISTEMA")
    print("=" * 40)

    # Testar carregamento de módulos
    if not testar_modulos():
        return False

    # Testar função de cache do GET
    print("\n📡 Testando sistema de cache...")
    try:
        sucesso = GET.carregar_formularios()
        if sucesso:
            print("✅ Cache de formulários funcionando!")

            # Teste de busca
            resultados = GET.buscar_clausulas(['1.5.1'], mostrar_detalhes=False)
            print(f"✅ Busca no cache funcionando! ({len(resultados)} resultados)")
        else:
            print("❌ Falha no sistema de cache.")
            return False

    except Exception as e:
        print(f"❌ Erro no teste de cache: {e}")
        return False

    print("\n✅ TESTE RÁPIDO CONCLUÍDO COM SUCESSO!")
    print("💡 Execute 'python main.py' para iniciar o servidor completo.")
    return True


if __name__ == "__main__":
    # Verificar argumentos da linha de comando
    if len(sys.argv) > 1 and sys.argv[1] == "--teste":
        # Modo de teste rápido
        executar_teste_rapido()
    else:
        # Modo normal - iniciar servidor completo
        main()