from contract_templates.chatbot_template import generate_chatbot_assets
from contract_templates.data_analysis_template import generate_data_analysis_assets
from contract_templates.tutor_template import generate_tutor_assets


def generate_assets(scope_data: dict, plan_data: dict):
    project_type = scope_data.get("project_type", "")

    if project_type == "chatbot":
        return generate_chatbot_assets(scope_data, plan_data)
    if project_type == "data_analysis":
        return generate_data_analysis_assets(scope_data, plan_data)
    if project_type == "ai_tutor":
        return generate_tutor_assets(scope_data, plan_data)

    return []