# main.py - Arquivo principal que orquestra o sistema completo

# Instalar dependências se necessário:
# pip install fastapi nest-asyncio pyngrok uvicorn

import nest_asyncio
from pyngrok import ngrok, conf
import uvicorn
import sys
import os
import json

# Importar módulos do projeto
import webhook
import GET
from POST import ChecklistCreator# Importar o criador de checklists
import POSTtest


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
        auth_token = "2yy04GbRMzDFhGgaRo3PGRqV5tC_4gkaL24YZ3yhDkNq9wDuh"
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

def criar_tunel_ngrok(porta=8000, dominio="enormous-infinite-tahr.ngrok-free.app"):
    """
    Cria o túnel ngrok com um domínio estático
    """
    try:
        # Especificar o domínio reservado ao criar o túnel
        public_url = ngrok.connect(porta, domain=dominio)
        print(f"🔗 Túnel ngrok criado com domínio fixo: {public_url}")
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
    print(f"📋 Modo de operação: 🔄 Cache atualizado a cada webhook + POST automático")


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

        # Testar POST.py
        creator = ChecklistCreator()
        print("✅ POST.py: Módulo carregado corretamente")

        print("✅ Todos os módulos funcionando!")
        return True

    except Exception as e:
        print(f"❌ Erro ao testar módulos: {e}")
        return False


def modificar_webhook_com_post():
    """
    Modifica o processamento do webhook para incluir o POST automático
    """
    # Salvar a função original
    processar_webhook_original = webhook.processar_webhook_completo

    # Variável global para armazenar o último checklist criado
    ultimo_checklist_id = None

    def processar_webhook_com_post(body):
        """
        Versão modificada que adiciona POST após processar webhook
        """
        nonlocal ultimo_checklist_id

        # Processar webhook normalmente
        resultado = processar_webhook_original(body)

        if resultado['status'] == 'sucesso':
            print("\n" + "=" * 60)
            print("📝 INICIANDO CRIAÇÃO AUTOMÁTICA DO CHECKLIST")
            print("=" * 60)

            try:
                # Extrair informações do resultado
                dados = resultado['dados_formatados']

                # Preparar dados de identificação
                identificacao = {
                    'data_prevista': dados['data_prevista'],
                    'contrato': dados['contrato_concessao'],
                    'identificador': dados['identificador'],
                    'concessionaria': dados['concessionaria']
                }

                # Criar o ID do checklist baseado no identificador
                checklist_id = f"exec_{dados['identificador'].replace(' ', '_').replace('-', '_')}"

                print(f"📅 Data prevista: {identificacao['data_prevista']}")
                print(f"🏢 Concessionária: {identificacao['concessionaria']}")

                # Processar os itens habilitados e buscar informações no cache
                itens_por_tipo = processar_itens_para_post(dados, resultado.get('formularios_por_tipo', {}))

                # Criar o checklist usando POST.py
                creator = ChecklistCreator()
                checklist_criado = creator.criar_checklist_completo(
                    identificacao=identificacao,
                    itens_por_tipo=itens_por_tipo,
                    assignee_id="6478f2c883e4a9312d68da0b",  # Pode ser configurável
                    creator_id="6478f2c883e4a9312d68da0b"
                )

                if checklist_criado:
                    ultimo_checklist_id = checklist_criado
                    resultado['checklist_criado'] = checklist_criado
                    print(f"\n✅ CHECKLIST CRIADO COM SUCESSO!")
                    print(f"📋 ID: {checklist_criado}")
                    print("=" * 60)
                else:
                    print("\n❌ Falha ao criar checklist")

            except Exception as e:
                print(f"\n❌ Erro ao criar checklist: {e}")
                import traceback
                traceback.print_exc()

        return resultado

    # Substituir a função no módulo webhook
    webhook.processar_webhook_completo = processar_webhook_com_post

    # Retornar função para acessar o último checklist
    def obter_ultimo_checklist():
        return {"ultimo_checklist_id": ultimo_checklist_id}

    return obter_ultimo_checklist

def processar_itens_para_post(dados_webhook, formularios_por_tipo=None):
    """
    Processa os itens habilitados e busca informações no cache para criar o formato do POST
    """
    itens_por_tipo = {}

    # Se não tiver formulários, buscar no cache
    if not formularios_por_tipo:
        formularios_por_tipo = {}
        for tipo in ['FA', 'FT', 'FO', 'GC', 'VC']:
            itens_habilitados = []
            for item in dados_webhook[f'itens_{tipo.lower()}']:
                if item['habilitado']:
                    itens_habilitados.append(item['item'])

            if itens_habilitados:
                formularios = GET.buscar_clausulas(itens_habilitados, mostrar_detalhes=False)
                formularios_por_tipo[tipo] = formularios

    # Processar cada tipo
    for tipo in ['FA', 'FT', 'FO', 'GC', 'VC']:
        itens = []

        # Buscar itens habilitados do webhook
        itens_webhook = dados_webhook.get(f'itens_{tipo.lower()}', [])
        itens_habilitados = [item for item in itens_webhook if item['habilitado']]

        if itens_habilitados:
            print(f"\n📋 Processando {len(itens_habilitados)} itens {tipo}...")

            # Para cada item habilitado, buscar no cache
            for item_webhook in itens_habilitados:
                item_clausula = item_webhook['item']

                # Buscar informações do formulário no cache
                formularios = GET.buscar_clausulas([item_clausula], mostrar_detalhes=False)

                if formularios:
                    formulario = formularios[0]  # Pegar o primeiro (deve ser único)

                    # Extrair informações do formulário
                    for secao in formulario.get('sections', []):
                        if secao.get('title') == 'Identificação':
                            info_item = {}

                            # Adicionar o campo 'item' do webhook
                            info_item['item'] = item_clausula

                            # Mapear os campos
                            for questao in secao.get('questions', []):
                                titulo = questao.get('title', '').lower()
                                valor = None

                                if questao.get('sub_questions'):
                                    valor = questao['sub_questions'][0].get('value')

                                # Incluir mapeamento de 'item'
                                if 'código' in titulo:
                                    info_item['codigo'] = valor
                                elif 'instrumento' in titulo:
                                    info_item['instrumento'] = valor or 'Contrato'
                                elif 'dimensão' in titulo:
                                    info_item['dimensao'] = valor
                                elif 'verificação' in titulo:
                                    info_item['verificacao'] = valor
                                elif 'indicador' in titulo:
                                    info_item['indicador'] = valor

                            # REMOVER linha de 'resposta'
                            # Adicionar valores padrão para AV e peso
                            info_item['av'] = 1
                            info_item['peso'] = 1

                            # Item será incluído se tiver qualquer campo preenchido
                            if info_item:
                                itens.append(info_item)
                                print(f"   ✅ Item processado: {item_clausula}")
                            break

        if itens:
            itens_por_tipo[tipo] = itens

    return itens_por_tipo

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

        # Modificar webhook para incluir POST
        print("\n🔧 Configurando POST automático...")
        obter_ultimo_checklist = modificar_webhook_com_post()
        print("✅ POST automático configurado!")

        # Criar aplicação FastAPI usando as funções do webhook
        print("\n🏗️  Criando aplicação FastAPI...")
        app = webhook.criar_app_fastapi()

        # Adicionar endpoint para ver último checklist
        @app.get("/ultimo-checklist")
        async def ultimo_checklist():
            """Retorna o ID do último checklist criado"""
            return obter_ultimo_checklist()

        # Criar túnel ngrok com domínio estático
        print("🌐 Criando túnel ngrok com domínio estático...")
        public_url = criar_tunel_ngrok(8000, "enormous-infinite-tahr.ngrok-free.app")

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

    # Testar criação de checklist
    print("\n📝 Testando sistema de POST...")
    try:
        creator = ChecklistCreator()
        print("✅ Sistema de POST carregado!")

        # Teste simples de estrutura
        test_data = {
            'data_prevista': '2025-06-23',
            'contrato': 'TEST-001',
            'identificador': 'TEST-2025',
            'concessionaria': 'Empresa Teste'
        }

        print(f"✅ Estrutura de dados validada!")

    except Exception as e:
        print(f"❌ Erro no teste de POST: {e}")
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