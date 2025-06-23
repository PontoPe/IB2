import requests
import json

# URL e parâmetros
url = "https://app.way-v.com/api/integration/form_entries"
params = {
    "execution_company_id": "663d31a1e9dac3f5f4d3cf2e",
    "template_id": "67f6bfe0aa27d85466bdbb87"
}
headers = {
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb21wYW55X2lkIjoiNjYzZDMxYTFlOWRhYzNmNWY0ZDNjZjJlIiwiY3VycmVudF90aW1lIjoxNzQ4OTUzODcyNjgzLCJleHAiOjIwNjQ0ODY2NzJ9.j6zOrJMDKNcCcMMcO99SudriP7KqEDLMJDE2FBlQ6ok",
    "Content-Type": "application/json"
}

response = requests.get(url, headers=headers, params=params)
print(response.text)
if response.status_code == 200:
    data = response.json()
    entries = data.get("form_entries", [])

    for entry in entries:
        entry_id = entry.get("_id", "sem ID")
        print(f"\n📋 Checklist ID: {entry_id}")

        # Campos principais do checklist
        for item in entry.get("form_entry_columns", []):
            section_title = item.get("section", {}).get("title", "Sem título de seção")
            question_key = item.get("key", "")
            question_text = item.get("text", "")
            value = item.get("value")

            print(f"  📂 Seção: {section_title}")
            print(f"    ❓ Pergunta: {question_text} | ID: {question_key} | Valor: {value}")

        # Subformulários (subchecklists dentro do checklist)
        for item in entry.get("form_entry_columns", []):
            if item.get("type") == "sub_form":
                subform_section = item.get("section", {}).get("title", "Subseção")
                print(f"\n  🔁 Subformulário da seção: {subform_section}")

                for sub_entry in item.get("sub_form_entries", []):
                    sub_id = sub_entry.get("_id", "sem ID")
                    print(f"    ➕ Subentrada ID: {sub_id}")

                    for sub_col in sub_entry.get("sub_entries_columns", []):
                        key = sub_col.get("key", "")
                        text = sub_col.get("text", "")
                        value = sub_col.get("value", "")
                        print(f"      ➥ Subitem: {text} | ID: {key} | Valor: {value}")

        print("-" * 60)

else:
    print(f"❌ Erro {response.status_code}")
    print(response.text)