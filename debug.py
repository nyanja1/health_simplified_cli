
from typer.testing import CliRunner
from health_tracker.cli import app
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from health_tracker.models import Base, User, FoodEntry, Goal, MealPlan
from health_tracker.database import engine

runner = CliRunner()

def test_cli_commands():
    """Test all CLI commands and edge cases for debugging."""
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

    # Update food entry
    result = runner.invoke(app, ["entry-update", "--id", "1", "--food", "Cheese Pizza", "--calories", "600"])
    assert result.exit_code == 0, f"Failed to update food entry: {result.output}"
    assert "Food entry ID 1 updated successfully" in result.output

    # Delete food entry
    result = runner.invoke(app, ["entry-delete", "--id", "1"])
    assert result.exit_code == 0, f"Failed to delete food entry: {result.output}"
    assert "Food entry ID 1 deleted successfully" in result.output

    # Set goal
    result = runner.invoke(app, ["goal-set", "--user", "Elvis", "--daily-calories", "2000", "--weekly-calories", "14000"])
    assert result.exit_code == 0, f"Failed to set goal: {result.output}"
    assert "Goal set for user 'Elvis'" in result.output

    # List goals
    result = runner.invoke(app, ["goal-list"])
    assert result.exit_code == 0, f"Failed to list goals: {result.output}"
    assert "Daily Calories: 2000" in result.output
    assert "Weekly Calories: 14000" in result.output

    # Create meal plan
    result = runner.invoke(app, ["plan-meal", "--user", "Elvis", "--week", "22", "--meals", "Mon: Salad, Tue: Pasta"])
    assert result.exit_code == 0, f"Failed to create meal plan: {result.output}"
    assert "Meal plan created for user 'Elvis' for week 22" in result.output

    # Generate report
    result = runner.invoke(app, ["report", "--user", "Elvis", "--start-date", "2025-05-29", "--end-date", "2025-05-29"])
    assert result.exit_code == 0, f"Failed to generate report: {result.output}"
    assert "Total Calories: 0" in result.output  # No entries after deletion
    assert "Daily: 2000" in result.output
    assert "Week: 22" in result.output

    # Verify database state
    with Session(engine) as session:
        user = session.execute(select(User).filter_by(name="Elvis")).scalar_one()
        assert user.name == "Elvis"
        entries = session.execute(select(FoodEntry).filter_by(user_id=user.id)).scalars().all()
        assert len(entries) == 0, "Food entries should be deleted"
        goal = session.execute(select(Goal).filter_by(user_id=user.id)).scalar_one()
        assert goal.daily_calories == 2000
        plan = session.execute(select(MealPlan).filter_by(week_number=22)).scalar_one()
        assert plan.meals == "Mon: Salad, Tue: Pasta"

    # Test invalid inputs
    result = runner.invoke(app, ["user-create", "--name", ""])
    assert result.exit_code == 1, f"Expected error for empty name: {result.output}"
    assert "Error: Name must be a non-empty string" in result.output

    result = runner.invoke(app, ["entry-add", "--user", "Elvis", "--food", "Pizza", "--calories", "-100", "--date", "2025-05-29"])
    assert result.exit_code == 1, f"Expected error for negative calories: {result.output}"
    assert "Error: Calories must be a positive integer" in result.output

    result = runner.invoke(app, ["entry-add", "--user", "Unknown", "--food", "Pizza", "--calories", "500", "--date", "2025-05-29"])
    assert result.exit_code == 1, f"Expected error for unknown user: {result.output}"
    assert "Error: User 'Unknown' not found" in result.output

    result = runner.invoke(app, ["entry-list", "--date", "invalid"])
    assert result.exit_code == 1, f"Expected error for invalid date: {result.output}"
    assert "Error: Invalid date format" in result.output

    result = runner.invoke(app, ["goal-set", "--user", "Elvis", "--daily-calories", "-2000", "--weekly-calories", "14000"])
    assert result.exit_code == 1, f"Expected error for negative daily calories: {result.output}"
    assert "Error: Daily calories must be a positive integer" in result.output

    result = runner.invoke(app, ["plan-meal", "--user", "Elvis", "--week", "-1", "--meals", "Mon: Salad"])
    assert result.exit_code == 1, f"Expected error for negative week: {result.output}"
    assert "Error: Week number must be a positive integer" in result.output

    result = runner.invoke(app, ["report", "--start-date", "2025-05-30", "--end-date", "2025-05-29"])
    assert result.exit_code == 1, f"Expected error for invalid date range: {result.output}"
    assert "Error: Start date must be before end date" in result.output

if __name__ == "__main__":
    test_cli_commands()
    print("Debug script completed successfully.")
