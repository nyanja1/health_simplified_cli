```python
from typer.testing import CliRunner
from health_tracker.cli import app
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from health_tracker.models import Base, User, FoodEntry, Goal, MealPlan
from health_tracker.database import engine

runner = CliRunner()

def test_cli_commands():
    # Create user
    result = runner.invoke(app, ["user-create", "--name", "Elvis"])
    assert result.exit_code == 0, f"Failed to create user: {result.output}"
    assert "User 'Elvis' created successfully" in result.output

    # List users
    result = runner.invoke(app, ["user-list"])
    assert result.exit_code == 0, f"Failed to list users: {result.output}"
    assert "Name: Elvis" in result.output

    # Add food entry
    result = runner.invoke(app, ["entry-add", "--user", "Elvis", "--food", "Pizza", "--calories", "500", "--date", "2025-05-29"])
    assert result.exit_code == 0, f"Failed to add food entry: {result.output}"
    assert "Food entry added: Pizza (500 calories) for Elvis on 2025-05-29" in result.output

    # List food entries
    result = runner.invoke(app, ["entry-list"])
    assert result.exit_code == 0, f"Failed to list food entries: {result.output}"
    assert "Food: Pizza" in result.output
    assert "Calories: 500" in result.output

    # Verify data in database
    with Session(engine) as session:
        user = session.execute(select(User).filter_by(name="Elvis")).scalar_one()
        assert user.name == "Elvis"
        entry = session.execute(select(FoodEntry).filter_by(food="Pizza")).scalar_one()
        assert entry.calories == 500
        assert str(entry.date) == "2025-05-29"

    # Test invalid inputs
    result = runner.invoke(app, ["user-create", "--name", ""])
    assert result.exit_code == 1, f"Expected error for empty name: {result.output}"
    assert "Error: Name must be a non-empty string" in result.output

    result = runner.invoke(app, ["entry-add", "--user", "Elvis", "--food", "Pizza", "--calories", "-100", "--date", "2025-05-29"])
    assert result.exit_code == 1, f"Expected error for negative calories: {result.output}"
    assert "Error: Calories must be a positive integer" in result.output

    result = runner.invoke(app, ["entry-add", "--user", "Elvis", "--food", "", "--calories", "500", "--date", "2025-05-29"])
    assert result.exit_code == 1, f"Expected error for empty food: {result.output}"
    assert "Error: Food must be a non-empty string" in result.output

if __name__ == "__main__":
    test_cli_commands()
    print("Debug script completed successfully.")
```