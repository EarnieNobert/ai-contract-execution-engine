def generate_data_analysis_assets(scope_data: dict, plan_data: dict):
    return [
        {
            "artifact_type": "markdown",
            "filename": "analysis_scope.md",
            "content": f"# Data Analysis Scope\n\nGoal: {scope_data.get('goal', '')}\n"
        },
        {
            "artifact_type": "markdown",
            "filename": "data_cleaning_plan.md",
            "content": "# Data Cleaning Plan\n\n- Check missing values\n- Standardize column names\n- Inspect data types\n- Remove duplicates if needed\n"
        },
        {
            "artifact_type": "python",
            "filename": "starter_analysis.py",
            "content": """import pandas as pd

def load_data(path):
    df = pd.read_csv(path)
    return df

if __name__ == "__main__":
    print("Starter analysis script ready.")
"""
        }
    ]