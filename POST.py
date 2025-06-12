#fazer novo Checklist com as informacoes obtidas anteriormenteimport requests
import time
import json

# Token e cabeçalhos
token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb21wYW55X2lkIjoiNjYzZDMxYTFlOWRhYzNmNWY0ZDNjZjJlIiwiY3VycmVudF90aW1lIjoxNzQ4OTUzODcyNjgzLCJleHAiOjIwNjQ0ODY2NzJ9.j6zOrJMDKNcCcMMcO99SudriP7KqEDLMJDE2FBlQ6ok'
headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Authorization": f"Bearer {token}"
}

# URLs de integração
checklist_url = "https://app.way-v.com/api/integration/checklists"
subchecklist_url = "https://app.way-v.com/api/integration/subchecklists"

# Payload de checklist principal
checklist_payload = {

    "checklist_columns": [
        {
            "question_key": QUESTION1_KEY,
            "value": QUESTION1_VAL
        },
        {
            "question_key": QUESTION2_KEY,
            "value": QUESTION2_VAL
        },
        {
            "question_key": QUESTION3_KEY,
            "value": QUESTION3_VAL
        },
        {
            "question_key": QUESTION4_KEY,
            "value": QUESTION4_VAL
        }
    ]
}

# 1. Cria o checklist
response = requests.post(checklist_url, headers=headers, json=checklist_payload)

if response.status_code == 201:
    checklist_id = response.json()["_id"]["$oid"]
    print(f"✅ Checklist criado: {checklist_id}")
    time.sleep(5)

    # 2. Cria subchecklists
    sub_payload = {
        "checklist_id": checklist_id,
        "sub_checklists": [
            {
                "id": SUBCHECKLISTS1_ID,  # ID do tipo de subchecklist
                "sub_checklist_questions": [
                    {
                        "question_id": SUBCHECKLISTS1_QUESTION1_ID,  
                        "value": SUBCHECKLISTS1_QUESTION1_VAL
                    },
                    {
                        "question_id": SUBCHECKLISTS1_QUESTION2_ID,  
                        "value": SUBCHECKLISTS1_QUESTION2_VAL
                    }
                ]
            },
            {
                "id": SUBCHECKLISTS1_ID, #Outro item, mas mesmo tipo de subchecklist, entao mesmo ID de subchecklist
                "sub_checklist_questions": [
                    {
                        "question_id": SUBCHECKLISTS1_QUESTION1_ID,
                        "value": SUBCHECKLISTS1_QUESTION1_VAL
                    },
                    {
                        "question_id": SUBCHECKLISTS1_QUESTION2_ID, 
                        "value": SUBCHECKLISTS1_QUESTION2_VAL
                    }
                ]
            }
        ]
    }

    sub_response = requests.post(subchecklist_url, headers=headers, json=sub_payload)
    if sub_response.status_code == 201:
        print("✅ Subchecklists criados com sucesso!")
    else:
        print(f"⚠ Erro ao criar subchecklists: {sub_response.status_code}")
        print(sub_response.text)
else:
    print(f"❌ Erro ao criar checklist: {response.status_code}")
    print("Payload enviado:")
    print(json.dumps(checklist_payload, indent=2))
    print("Resposta da API:")
    print(response.text)
