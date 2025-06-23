import requests
import json
from datetime import datetime
from typing import Dict, List, Optional


class ChecklistCreator:
    def __init__(self):
        self.base_url = "https://app.way-v.com/api/integration"
        self.token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb21wYW55X2lkIjoiNjYzZDMxYTFlOWRhYzNmNWY0ZDNjZjJlIiwiY3VycmVudF90aW1lIjoxNzQ4OTUzODcyNjgzLCJleHAiOjIwNjQ0ODY2NzJ9.j6zOrJMDKNcCcMMcO99SudriP7KqEDLMJDE2FBlQ6ok'
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

        # IDs fixos do template de execução
        self.template_id = "67f6ae4d6ba4f07ba32a1ea8"  # Template de execução
        self.execution_company_id = "663d31a1e9dac3f5f4d3cf2e"

        # IDs das perguntas principais para adicionar itens
        self.question_ids = {
            'FA': '934f80ddd425479b969227c01a5c2eda',
            'FT': '9ef230b33c3c435fbe83298d41acc30a',
            'FO': '8c517d351f15462aa62b4c9ac7e6b43e',
            'GC': '6e6de895e4604ba78f18e154072be80e',
            'VC': '438dc9b0b7394a72b6ff5008d7574824'
        }

        # Mapeamento dos IDs das sub-perguntas para cada tipo
        self.sub_question_mapping = {
            'FA': {
                'item': '1698387cdcd94042b978a272d7248fb8',
                'codigo': '5a507221009d479a87fe3ac2de9b1919',
                'instrumento': 'b97d97f46fc04c15a2c301949d1b8861',
                'dimensao': '3c12a83a05b7482193cbf32d511c864e',
                'verificacao': 'e758f7b11b2e4d4f99eea9520711a8b1',
                'resposta': '9e3dc6b89ba24d899b20a30a00eefea6',
                'av': '25022d88d8d342c7bb81e77896378032',
                'peso': 'fd2cc26145c64297b55f002f5552fb8d',
                'avp': '1a13b936644f4eaf8f65033b24fb2daf',
                'indicador': '68015fa3daf29bba925f3db7'
            },
            'FT': {
                'item': 'd762bd3540d14de799e31645a451d37b',
                'codigo': '61a996bc1fc34a79a057337493e40b82',
                'instrumento': 'b2a7a4c6f8e147f4a05ec7078f8fa701',
                'dimensao': '340e1d43c30f44c688feb46a2a67804e',
                'verificacao': 'af52a22123a64a5c90cea2d9879ecc8a',
                'indicador': 'a2a45ba1f55f47a5919371ad569afc15',
                'resposta': '02b1be56056e4e6d9fb92535738c1ec2',
                'av': '5b424d95b0564b8e8d7c5794b4339ef5',
                'peso': '3f6a015c3b2a4c9fa34b9e243d55f54d',
                'avp': '755a8a013f834a47b1e38616ca4cb940'
            },
            'FO': {
                'item': 'f2430b29128a4c34ad5e01b7b6b05590',
                'codigo': '683f4b1dc4a5538b711b0f01',
                'instrumento': '18d14859aacf40f8a1ef25e42444c969',
                'dimensao': '83a2870b2f7845aaab120084d5337ac7',
                'verificacao': '5904a66402a44734b20404dd51d2f95c',
                'indicador': '4435bc77d6234f0d85cf73ea2ac3992b',
                'resposta': '3319075725da42e99a3adf15b9267c9f',
                'av': '4dbab1cc69714abba9c7d71a334a7681',
                'peso': 'a750de10487c4a0a9483992b9062456f',
                'avp': '8dad2e71fbf94e1ab1249756a8ff96eb'
            },
            'GC': {
                'item': '835fef882525445fbf2559bf9c00083b',
                'instrumento': '1a40fe0f826841da8b43ffeba3c1eeae',
                'codigo': '683f4f9f6019b1f3b94bbeff',
                'dimensao': '597dcedfa3a9431d997dfca22f19dd1d',
                'verificacao': 'e4b50d1f4165477fa7902d033700dd88',
                'indicador': '57e1268b630149998a83e568372b3453',
                'resposta': '142585450e314b5992bcf9913f092647',
                'av': '16094d6622e547b18655731a5b2d4078',
                'peso': 'ca2286fe3f784b568deb19c85e3242b3',
                'avp': '1d9c6ac747de4b6d96c9e7ed02b3a350'
            },
            'VC': {
                'item': 'fa60b9d2d76e4c4aaac5e9abc4fe0fcc',
                'instrumento': '5a1e10805d00494eaa8b8f84b321e4d0',
                'codigo': '683f51034c5aa9678b216f1e',
                'dimensao': '954901ca7d034cb7ae6695ba36497cdc',
                'verificacao': 'c81768535b3f4ded9ca03b6302d1fbe1',
                'indicador': '4466ffcbe37b4506b42922a9e6743fc8',
                'resposta': 'a1808fca95e14ffa9f673857500f708e',
                'av': '388a99bb2c8d47ce8abd5d1e7f4a2ca1',
                'peso': '3396de2bc98447b1b339a937056bfc30',
                'avp': '175178e731144088b56897910ffd3531'
            }
        }

        # IDs das perguntas de identificação
        self.identification_questions = {
            'data_prevista': '8113d0edd61c4cf6bf65ec10bdf68cda',
            'contrato': '11caa9daefcd41bcade0fb221886758b',
            'identificador': 'ed1c45973cfd47cbbd13fb26ff448e16',
            'concessionaria': '8838d1ca06bb4e0ba842b0e1adc5d949'
        }

    def criar_checklist(self,
                        checklist_id: str,
                        identificacao: Dict[str, str],
                        itens_por_tipo: Dict[str, List[Dict]],
                        assignee_id: str = None,
                        creator_id: str = None):
        """
        Cria um checklist completo com os itens especificados

        Args:
            checklist_id: ID do checklist (usar o mesmo para atualizar)
            identificacao: Dict com data_prevista, contrato, identificador, concessionaria
            itens_por_tipo: Dict onde a chave é o tipo (FA, FT, etc) e o valor é lista de itens
            assignee_id: ID do responsável
            creator_id: ID do criador

        Exemplo de itens_por_tipo:
        {
            'FT': [
                {
                    'item': '10.2',
                    'codigo': '03.04.05.03',
                    'instrumento': 'Contrato',
                    'dimensao': 'FINANCEIRA',
                    'verificacao': 'O Concessionário vem aplicando...',
                    'indicador': 'IECOMPR',
                    'resposta': 'Houve poucos registros',
                    'av': 3,
                    'peso': 2
                }
            ]
        }
        """

        # Estrutura base do checklist
        checklist_data = {
            "checklist": {
                "id": checklist_id,
                "template_id": self.template_id,
                "execution_company_id": self.execution_company_id,
                "assignee_id": assignee_id,
                "creator_id": creator_id,
                "status_info": {
                    "new_execution_status": "in_progress"
                },
                "questions": []
            }
        }

        # Adicionar perguntas de identificação
        for campo, question_id in self.identification_questions.items():
            if campo in identificacao:
                checklist_data["checklist"]["questions"].append({
                    "id": question_id,
                    "sub_questions": [{
                        "id": "1",
                        "value": identificacao[campo]
                    }]
                })

        # Adicionar perguntas de verificação (mesmo sem itens)
        for tipo in ['FA', 'FT', 'FO', 'GC', 'VC']:
            checklist_data["checklist"]["questions"].append({
                "id": self.question_ids[tipo],
                "sub_questions": []  # Vazio se não houver itens
            })

        # Primeiro criar o checklist principal
        print(f"📝 Criando checklist principal {checklist_id}...")
        response = requests.post(
            f"{self.base_url}/checklists",
            headers=self.headers,
            json=checklist_data
        )

        if response.status_code not in [200, 201]:
            print(f"❌ Erro ao criar checklist: {response.status_code}")
            print(response.text)
            return None

        print(f"✅ Checklist principal criado/atualizado!")

        # Agora criar os subchecklists para cada tipo com itens
        for tipo, itens in itens_por_tipo.items():
            if itens:
                print(f"\n📋 Criando {len(itens)} subchecklists para {tipo}...")
                self._criar_subchecklists(checklist_id, tipo, itens)

        return checklist_id

    def _criar_subchecklists(self, checklist_id: str, tipo: str, itens: List[Dict]):
        """
        Cria subchecklists para um tipo específico
        """
        sub_checklists = []
        question_mapping = self.sub_question_mapping[tipo]

        for item_data in itens:
            # Gerar um ID único para o subchecklist
            sub_checklist_id = self._gerar_subchecklist_id()

            # Construir as sub_questions baseado nos dados do item
            sub_questions = []

            # Adicionar cada campo do item
            for campo, question_id in question_mapping.items():
                if campo in item_data:
                    valor = str(item_data[campo])

                    # Calcular AV*P se for o campo avp
                    if campo == 'avp' and 'av' in item_data and 'peso' in item_data:
                        valor = str(item_data['av'] * item_data['peso'])

                    sub_questions.append({
                        "question_id": question_id,
                        "value": valor
                    })

            sub_checklists.append({
                "id": self.question_ids[tipo],  # ID da pergunta principal
                "sub_checklist_questions": sub_questions
            })

        # Fazer POST para criar os subchecklists
        payload = {
            "checklist_id": checklist_id,
            "sub_checklists": sub_checklists
        }

        response = requests.post(
            f"{self.base_url}/subchecklists",
            headers=self.headers,
            json=payload
        )

        if response.status_code in [200, 201]:
            print(f"✅ {len(itens)} subchecklists criados para {tipo}")
        else:
            print(f"❌ Erro ao criar subchecklists para {tipo}: {response.status_code}")
            print(response.text)

    def _gerar_subchecklist_id(self):
        """Gera um ID único para subchecklist"""
        import uuid
        return str(uuid.uuid4()).replace('-', '')


# Exemplo de uso
if __name__ == "__main__":
    creator = ChecklistCreator()

    # Dados de identificação
    identificacao = {
        "data_prevista": "2025-02-15",
        "contrato": "CTR-2025-001",
        "identificador": "PLAN-2025-02",
        "concessionaria": "Empresa XYZ"
    }

    # Exemplo 1: Criar checklist apenas com itens FT
    print("=== EXEMPLO 1: Apenas itens FT ===")
    itens_ft = [
        {
            'item': '10.2',
            'codigo': '03.04.05.03',
            'instrumento': 'Contrato',
            'dimensao': 'FINANCEIRA',
            'verificacao': 'O Concessionário vem aplicando os descontos e isenções previstas em Lei?',
            'indicador': 'IECOMPR',
            'resposta': 'Houve poucos registros',
            'av': 3,
            'peso': 2
        },
        {
            'item': '11',
            'codigo': '03.04.05.04',
            'instrumento': 'Contrato',
            'dimensao': 'FINANCEIRA',
            'verificacao': 'O Concessionário tem pago as outorgas rigorosamente corretamente?',
            'indicador': 'IESOLV',
            'resposta': 'Não houve registro',
            'av': 5,
            'peso': 3
        }
    ]

    checklist_id_1 = "teste_checklist_001"
    creator.criar_checklist(
        checklist_id=checklist_id_1,
        identificacao=identificacao,
        itens_por_tipo={'FT': itens_ft},
        assignee_id="6478f2c883e4a9312d68da0b",
        creator_id="6478f2c883e4a9312d68da0b"
    )

    # Exemplo 2: Criar checklist com todos os tipos
    print("\n\n=== EXEMPLO 2: Todos os tipos de itens ===")
    todos_itens = {
        'FA': [
            {
                'item': '12.1.1.3',
                'codigo': '03.04.01.03',
                'instrumento': 'Contrato',
                'dimensao': 'SÓCIO-AMBIENTAL',
                'verificacao': 'O Concessionário implantou Programa Interpretativo?',
                'resposta': 'Houve um registro',
                'av': 4,
                'peso': 3,
                'indicador': 'IERI'
            }
        ],
        'FT': itens_ft,  # Reusar os itens FT do exemplo anterior
        'FO': [
            {
                'item': '12.1',
                'codigo': '03.04.01.01',
                'instrumento': 'Contrato',
                'dimensao': 'SÓCIO-AMBIENTAL',
                'verificacao': 'A Concessionário vem aplicando recursos nos Macrotemas?',
                'indicador': 'IECA',
                'resposta': 'Não aplicável no momento',
                'av': 1,
                'peso': 3
            }
        ],
        'GC': [
            {
                'item': '12.1.3.1',
                'instrumento': 'Contrato',
                'codigo': '03.04.01.09',
                'dimensao': 'SÓCIO-AMBIENTAL',
                'verificacao': 'A CONCESSIONÁRIA tem apoiado o desenvolvimento de projetos?',
                'indicador': 'IECA',
                'resposta': 'Sim, mas parcialmente',
                'av': 3,
                'peso': 3
            }
        ],
        'VC': [
            {
                'item': '12.1',
                'instrumento': 'Contrato',
                'codigo': '03.04.01.01',
                'dimensao': 'SÓCIO-AMBIENTAL',
                'verificacao': 'A Concessionário vem aplicando recursos nos Macrotemas?',
                'indicador': 'IECA',
                'resposta': 'Não aplicável no momento',
                'av': 1,
                'peso': 3
            }
        ]
    }

    checklist_id_2 = "teste_checklist_002"
    creator.criar_checklist(
        checklist_id=checklist_id_2,
        identificacao=identificacao,
        itens_por_tipo=todos_itens,
        assignee_id="6478f2c883e4a9312d68da0b",
        creator_id="6478f2c883e4a9312d68da0b"
    )