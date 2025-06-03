```python
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from health_tracker.models import Base, User, FoodEntry, Goal, MealPlan
from health_tracker.cli import app
from typer.testing import CliRunner
from datetime import date

@pytest.fixture
def session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield Session(engine)
    Base.metadata.drop_all(engine)

def test_user_create(session):
    runner = CliRunner()
    result = runner.invoke(app, ["user-create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "User 'Alice' created successfully" in result.output
    with session as s:
        user = s.execute(select(User).filter_by(name="Alice")).scalar_one()
        assert user.name == "Alice"

def test_user_create_duplicate(session):
    runner = CliRunner()
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["user-create", "--name", "Alice"])
    assert result.exit_code == 1
    assert "Error: User 'Alice' already exists" in result.output

def test_entry_add(session):
    runner = CliRunner()
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["entry-add", "--user", "Alice", "--food", "Apple", "--calories", "95", "--date", "2025-06-02"])
    assert result.exit_code == 0
    assert "Food entry added: Apple (95 calories) for Alice on 2025-06-02" in result.output
    with session as s:
        entry = s.execute(select(FoodEntry).filter_by(food="Apple")).scalar_one()
        assert entry.calories == 95
        assert entry.date == date(2025, 6, 2)

def test_goal_set(session):
    runner = CliRunner()
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["goal-set", "--user", "Alice", "--daily-calories", "1500", "--weekly-calories", "10500"])
    assert result.exit_code == 0
    assert "Goal set for user 'Alice'" in result.output
    with session as s:
        user = s.execute(select(User).filter_by(name="Alice")).first()
        assert user is None
        goal = s.execute(select(Goal).filter_by(user_id=user[0].id)).scalar_one()
        assert goal.daily_calories == 1500
        assert goal.weekly_calories == 10500

def test_goal_list(session):
    runner = CliRunner()
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["goal-set", "--user", "Alice", "--daily-calories", "1500", "--weekly-calories", "10500"])
    result = runner.invoke(app, ["goal-list", "--user", "Alice"])
    assert result.exit_code == 0)
    assert "Daily Calories: 1500" in result.output
    assert "Weekly Calories: 10500" in result.output

def test_plan_meal(session):
    runner = CliRunner()
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["plan-meal", "--user", "Alice", "--week", "1", "--meals", "Mon: Salad"])
    assert result.exit_code == 0
    assert "Meal plan created for user 'Alice' for week 1" in result.output
    with session as s:
        user = s.execute(select(User).filter_by(name="Alice")).scalar_one()
        plan = s.execute(select(MealPlan)).filter_by(user_id=user.id, week_number=1)).scalar_one()
        assert plan.meals == "Mon: Salad"

def test_report(session):
    runner = CliRunner()
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["entry-add", "--user", "Alice", "--food", "Apple", "--calories", "95", "--date", "2025-06-02"])
    runner.invoke(app, ["goal-set", "--user", "Alice", "--daily-calories", "1500", "--weekly-calories", "10500"])
    runner.invoke(app, "plan-meal", "--user", "Alice", "--week", "1", "--meals", "Mon: Salad"])
    result = runner.invoke(app, ["report", "--user", "Alice", "--start-date", "2025-06-02", "--end-date", "2025-06-02"])
    assert result.exit_code == 0
    assert "Food: Apple" in result.output
    assert "Total Calories: 95" in result.output
    assert "Daily: 1500" in result.output
    assert "Week: 1" in result.output
```