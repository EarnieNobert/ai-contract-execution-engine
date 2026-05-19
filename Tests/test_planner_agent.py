from contract_agents.planner_agent import generate_plan


def test_generate_plan():
    scope_data = {
        "project_type": "chatbot"
    }
    result = generate_plan(scope_data)

    assert len(result.milestones) > 0
    assert "Python" in result.recommended_stack