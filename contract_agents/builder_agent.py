import json

from contract_tools.llm_client import client
from contract_templates.chatbot_template import generate_chatbot_assets
from contract_templates.data_analysis_template import generate_data_analysis_assets
from contract_templates.tutor_template import generate_tutor_assets


def generate_assets_fallback(scope_data: dict, plan_data: dict):
    project_type = scope_data.get("project_type", "")

    if project_type == "chatbot":
        return generate_chatbot_assets(scope_data, plan_data)
    if project_type == "data_analysis":
        return generate_data_analysis_assets(scope_data, plan_data)
    if project_type == "ai_tutor":
        return generate_tutor_assets(scope_data, plan_data)

    return []


def generate_assets(scope_data: dict, plan_data: dict, use_ai: bool = True):
    if not use_ai:
        return generate_assets_fallback(scope_data, plan_data)

    system_prompt = """
You are the Builder Agent for an AI Contract Execution Engine.

Your job is to generate practical first-draft project assets based on the project scope and execution plan.

Supported project types:
- chatbot
- data_analysis
- ai_tutor

Generate 3 to 5 useful assets.

Rules:
- Every asset must have artifact_type, filename, content, and contract_type.
- Filenames must include extensions like .md, .json, or .py.
- Content should be useful as a real first draft.
- Do not claim the work is production-ready.
- Include human review reminders where appropriate.
"""

    user_prompt = f"""
Scope data:
{json.dumps(scope_data, indent=2)}

Plan data:
{json.dumps(plan_data, indent=2)}

Generate first-draft assets for this project.
"""

    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "asset_list_schema",
                    "schema": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": {
                            "assets": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "properties": {
                                        "artifact_type": {"type": "string"},
                                        "filename": {"type": "string"},
                                        "content": {"type": "string"},
                                        "contract_type": {"type": "string"}
                                    },
                                    "required": [
                                        "artifact_type",
                                        "filename",
                                        "content",
                                        "contract_type"
                                    ]
                                }
                            }
                        },
                        "required": ["assets"]
                    },
                    "strict": True
                }
            }
        )

        asset_dict = json.loads(response.output_text)
        return asset_dict.get("assets", [])

    except Exception as e:
        print(f"OpenAI builder failed. Falling back to template assets. Error: {e}")
        return generate_assets_fallback(scope_data, plan_data)