from contract_schemas.qa_schema import QASchema


def run_qa(scope_data: dict, plan_data: dict, assets: list) -> QASchema:
    missing_items = []
    risk_flags = []
    revision_suggestions = []

    if not scope_data.get("goal"):
        missing_items.append("Goal is missing from scope data.")

    if not plan_data.get("tasks"):
        missing_items.append("Execution tasks are missing.")

    if not assets:
        missing_items.append("No generated assets were found.")

    if scope_data.get("missing_info"):
        risk_flags.append("There is unresolved missing information from intake.")

    if len(assets) < 2:
        revision_suggestions.append("Generate more than one asset for a stronger first draft.")

    revision_suggestions.append("Review all generated outputs manually before client delivery.")

    coverage_score = max(0, 100 - (len(missing_items) * 20) - (len(risk_flags) * 10))
    ready_for_review = len(missing_items) == 0

    return QASchema(
        coverage_score=coverage_score,
        missing_items=missing_items,
        risk_flags=risk_flags,
        revision_suggestions=revision_suggestions,
        ready_for_review=ready_for_review
    )