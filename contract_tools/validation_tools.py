def validate_required_text(value: str) -> bool:
    return bool(value and value.strip())


def validate_project_type(value: str) -> bool:
    valid_types = [
        "chatbot",
        "data_analysis",
        "ai_tutor"
    ]
    return value in valid_types