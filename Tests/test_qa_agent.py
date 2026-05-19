from contract_agents.qa_agent import run_qa


def test_run_qa():
    scope_data = {"goal": "Build chatbot", "missing_info": []}
    plan_data = {"tasks": ["Task 1"]}
    assets = [{"filename": "file1.md", "content": "content"}]

    result = run_qa(scope_data, plan_data, assets)

    assert result.coverage_score >= 0