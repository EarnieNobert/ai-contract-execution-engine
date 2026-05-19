import os
from datetime import datetime
from contract_tools.file_tools import ensure_directory, write_text_file


def export_contract_package(contract_name: str, scope_data: dict, plan_data: dict, qa_data: dict, assets: list):
    safe_name = contract_name.strip().replace(" ", "_").lower() or "untitled_contract"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = os.path.join("outputs", f"{safe_name}_{timestamp}")

    ensure_directory(export_dir)
    ensure_directory(os.path.join(export_dir, "05_generated_assets"))

    write_text_file(
        os.path.join(export_dir, "01_project_summary.md"),
        f"# Project Summary\n\nContract Name: {scope_data.get('contract_name', '')}\n\nClient Name: {scope_data.get('client_name', '')}\n\nGoal: {scope_data.get('goal', '')}\n"
    )

    write_text_file(
        os.path.join(export_dir, "02_scope_and_assumptions.md"),
        f"# Scope and Assumptions\n\n## Deliverables\n{chr(10).join('- ' + x for x in scope_data.get('deliverables', []))}\n\n## Assumptions\n{chr(10).join('- ' + x for x in scope_data.get('assumptions', []))}\n\n## Missing Info\n{chr(10).join('- ' + x for x in scope_data.get('missing_info', []))}\n"
    )

    write_text_file(
        os.path.join(export_dir, "03_execution_plan.md"),
        f"# Execution Plan\n\n## Milestones\n{chr(10).join('- ' + x for x in plan_data.get('milestones', []))}\n\n## Tasks\n{chr(10).join('- ' + x for x in plan_data.get('tasks', []))}\n\n## Recommended Stack\n{chr(10).join('- ' + x for x in plan_data.get('recommended_stack', []))}\n"
    )

    write_text_file(
        os.path.join(export_dir, "04_risk_register.md"),
        f"# Risk Register\n\n{chr(10).join('- ' + x for x in plan_data.get('risk_register', []))}\n"
    )

    for asset in assets:
        filename = asset.get("filename", "untitled.txt")
        content = asset.get("content", "")
        write_text_file(os.path.join(export_dir, "05_generated_assets", filename), content)

    write_text_file(
        os.path.join(export_dir, "06_qa_report.md"),
        f"# QA Report\n\nCoverage Score: {qa_data.get('coverage_score', 0)}\n\n## Missing Items\n{chr(10).join('- ' + x for x in qa_data.get('missing_items', []))}\n\n## Risk Flags\n{chr(10).join('- ' + x for x in qa_data.get('risk_flags', []))}\n\n## Suggestions\n{chr(10).join('- ' + x for x in qa_data.get('revision_suggestions', []))}\n\nReady for Review: {qa_data.get('ready_for_review', False)}\n"
    )

    write_text_file(
        os.path.join(export_dir, "07_client_handoff.md"),
        "# Client Handoff\n\nThis folder contains the draft scope, execution plan, generated assets, and QA review for internal review before delivery.\n"
    )

    return export_dir