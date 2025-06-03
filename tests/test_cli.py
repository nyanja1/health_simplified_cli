
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
``````python
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from health_tracker.models import Base, User, FoodEntry, Goal, MealPlan
from health_tracker.cli import app
from typer.testing import CliRunner
from datetime import date

runner = CliRunner()

@pytest.fixture
def session():
    """Create a temporary in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield Session(engine)
    Base.metadata.drop_all(engine)

def test_user_create(session):
    """Test creating a user."""
    result = runner.invoke(app, ["user-create", "--name", "Alice"])
    assert result.exit_code == 0
    assert "User 'Alice' created successfully" in result.output
    with session as s:
        user = s.execute(select(User).filter_by(name="Alice")).scalar_one()
        assert user.name == "Alice"

def test_user_create_duplicate(session):
    """Test creating a duplicate user."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["user-create", "--name", "Alice"])
    assert result.exit_code == 1
    assert "Error: User 'Alice' already exists" in result.output

def test_user_create_invalid_name(session):
    """Test creating a user with an empty name."""
    result = runner.invoke(app, ["user-create", "--name", ""])
    assert result.exit_code == 1
    assert "Error: Name must be a non-empty string" in result.output

def test_user_list_empty(session):
    """Test listing users when none exist."""
    result = runner.invoke(app, ["user-list"])
    assert result.exit_code == 0
    assert "No users found" in result.output

def test_user_list(session):
    """Test listing users."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["user-list"])
    assert result.exit_code == 0
    assert "Name: Alice" in result.output

def test_entry_add(session):
    """Test adding a food entry."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["entry-add", "--user", "Alice", "--food", "Apple", "--calories", "95", "--date", "2025-06-02"])
    assert result.exit_code == 0
    assert "Food entry added: Apple (95 calories) for Alice on 2025-06-02" in result.output
    with session as s:
        entry = s.execute(select(FoodEntry).filter_by(food="Apple")).scalar_one()
        assert entry.calories == 95
        assert entry.date == date(2025, 6, 2)

def test_entry_add_invalid_user(session):
    """Test adding a food entry for a non-existent user."""
    result = runner.invoke(app, ["entry-add", "--user", "Unknown", "--food", "Apple", "--calories", "95", "--date", "2025-06-02"])
    assert result.exit_code == 1
    assert "Error: User 'Unknown' not found" in result.output

def test_entry_add_invalid_calories(session):
    """Test adding a food entry with negative calories."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["entry-add", "--user", "Alice", "--food", "Apple", "--calories", "-95", "--date", "2025-06-02"])
    assert result.exit_code == 1
    assert "Error: Calories must be a positive integer" in result.output

def test_entry_list_empty(session):
    """Test listing food entries when none exist."""
    result = runner.invoke(app, ["entry-list"])
    assert result.exit_code == 0
    assert "No food entries found" in result.output

def test_entry_list_filtered(session):
    """Test listing food entries with user and date filters."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["entry-add", "--user", "Alice", "--food", "Apple", "--calories", "95", "--date", "2025-06-02"])
    result = runner.invoke(app, ["entry-list", "--user", "Alice", "--date", "2025-06-02"])
    assert result.exit_code == 0
    assert "Food: Apple" in result.output

def test_entry_update(session):
    """Test updating a food entry."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["entry-add", "--user", "Alice", "--food", "Apple", "--calories", "95", "--date", "2025-06-02"])
    result = runner.invoke(app, ["entry-update", "--id", "1", "--food", "Banana", "--calories", "120"])
    assert result.exit_code == 0
    assert "Food entry ID 1 updated successfully" in result.output
    with session as s:
        entry = s.execute(select(FoodEntry).filter_by(id=1)).scalar_one()
        assert entry.food == "Banana"
        assert entry.calories == 120

def test_entry_update_invalid_id(session):
    """Test updating a non-existent food entry."""
    result = runner.invoke(app, ["entry-update", "--id", "999", "--food", "Banana"])
    assert result.exit_code == 1
    assert "Error: Food entry ID 999 not found" in result.output

def test_entry_delete(session):
    """Test deleting a food entry."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["entry-add", "--user", "Alice", "--food", "Apple", "--calories", "95", "--date", "2025-06-02"])
    result = runner.invoke(app, ["entry-delete", "--id", "1"])
    assert result.exit_code == 0
    assert "Food entry ID 1 deleted successfully" in result.output
    with session as s:
        entry = s.execute(select(FoodEntry).filter_by(id=1)).scalar_one_or_none()
        assert entry is None

def test_goal_set(session):
    """Test setting a goal."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["goal-set", "--user", "Alice", "--daily-calories", "1500", "--weekly-calories", "10500"])
    assert result.exit_code == 0
    assert "Goal set for user 'Alice'" in result.output
    with session as s:
        user = s.execute(select(User).filter_by(name="Alice")).scalar_one()
        goal = s.execute(select(Goal).filter_by(user_id=user.id)).scalar_one()
        assert goal.daily_calories == 1500
        assert goal.weekly_calories == 10500

def test_goal_set_update(session):
    """Test updating an existing goal."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["goal-set", "--user", "Alice", "--daily-calories", "1500", "--weekly-calories", "10500"])
    result = runner.invoke(app, ["goal-set", "--user", "Alice", "--daily-calories", "1600", "--weekly-calories", "11200"])
    assert result.exit_code == 0
    assert "Goal updated for user 'Alice'" in result.output
    with session as s:
        user = s.execute(select(User).filter_by(name="Alice")).scalar_one()
        goal = s.execute(select(Goal).filter_by(user_id=user.id)).scalar_one()
        assert goal.daily_calories == 1600
        assert goal.weekly_calories == 11200

def test_goal_list(session):
    """Test listing goals."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["goal-set", "--user", "Alice", "--daily-calories", "1500", "--weekly-calories", "10500"])
    result = runner.invoke(app, ["goal-list", "--user", "Alice"])
    assert result.exit_code == 0
    assert "Daily Calories: 1500" in result.output
    assert "Weekly Calories: 10500" in result.output

def test_plan_meal(session):
    """Test creating a meal plan."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    result = runner.invoke(app, ["plan-meal", "--user", "Alice", "--week", "1", "--meals", "Mon: Salad"])
    assert result.exit_code == 0
    assert "Meal plan created for user 'Alice' for week 1" in result.output
    with session as s:
        user = s.execute(select(User).filter_by(name="Alice")).scalar_one()
        plan = s.execute(select(MealPlan).filter_by(user_id=user.id, week_number=1)).scalar_one()
        assert plan.meals == "Mon: Salad"

def test_plan_meal_update(session):
    """Test updating a meal plan."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["plan-meal", "--user", "Alice", "--week", "1", "--meals", "Mon: Salad"])
    result = runner.invoke(app, ["plan-meal", "--user", "Alice", "--week", "1", "--meals", "Mon: Soup"])
    assert result.exit_code == 0
    assert "Meal plan updated for user 'Alice' for week 1" in result.output
    with session as s:
        user = s.execute(select(User).filter_by(name="Alice")).scalar_one()
        plan = s.execute(select(MealPlan).filter_by(user_id=user.id, week_number=1)).scalar_one()
        assert plan.meals == "Mon: Soup"

def test_report(session):
    """Test generating a report."""
    runner.invoke(app, ["user-create", "--name", "Alice"])
    runner.invoke(app, ["entry-add", "--user", "Alice", "--food", "Apple", "--calories", "95", "--date", "2025-06-02"])
    runner.invoke(app, ["goal-set", "--user", "Alice", "--daily-calories", "1500", "--weekly-calories", "10500"])
    runner.invoke(app, ["plan-meal", "--user", "Alice", "--week", "1", "--meals", "Mon: Salad"])
    result = runner.invoke(app, ["report", "--user", "Alice", "--start-date", "2025-06-02", "--end-date", "2025-06-02"])
    assert result.exit_code == 0
    assert "Food: Apple" in result.output
    assert "Total Calories: 95" in result.output
    assert "Daily: 1500" in result.output
    assert "Week: 1" in result.output
