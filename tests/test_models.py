
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from health_tracker.models import Base, User, FoodEntry, Goal, MealPlan
from datetime import date

@pytest.fixture
def session():
    """Create a temporary in-memory SQLite database for testing."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield Session(engine)
    Base.metadata.drop_all(engine)

def test_user_valid(session):
    """Test creating a valid User."""
    with session as s:
        user = User(name="Alice")
        s.add(user)
        s.commit()
        assert user.name == "Alice"

def test_user_invalid_name(session):
    """Test User with invalid name."""
    user = User(name="")
    assert user.name is None  # Validation prevents setting

def test_food_entry_valid(session):
    """Test creating a valid FoodEntry."""
    with session as s:
        user = User(name="Alice")
        s.add(user)
        s.commit()
        entry = FoodEntry(user=user, food="Apple", calories=95, date=date(2025, 6, 2))
        s.add(entry)
        s.commit()
        assert entry.food == "Apple"
        assert entry.calories == 95

def test_food_entry_invalid_calories(session):
    """Test FoodEntry with invalid calories."""
    with session as s:
        user = User(name="Alice")
        s.add(user)
        s.commit()
        entry = FoodEntry(user=user, food="Apple", calories=-95, date=date(2025, 6, 2))
        assert entry.calories is None  # Validation prevents setting

def test_goal_valid(session):
    """Test creating a valid Goal."""
    with session as s:
        user = User(name="Alice")
        s.add(user)
        s.commit()
        goal = Goal(user=user, daily_calories=1500, weekly_calories=10500)
        s.add(goal)
        s.commit()
        assert goal.daily_calories == 1500
        assert goal.weekly_calories == 10500

def test_goal_invalid_daily_calories(session):
    """Test Goal with invalid daily calories."""
    with session as s:
        user = User(name="Alice")
        s.add(user)
        s.commit()
        goal = Goal(user=user, daily_calories=-1500, weekly_calories=10500)
        assert goal.daily_calories is None  # Validation prevents setting

def test_meal_plan_valid(session):
    """Test creating a valid MealPlan."""
    with session as s:
        user = User(name="Alice")
        s.add(user)
        s.commit()
        plan = MealPlan(user=user, week_number=1, meals="Mon: Salad")
        s.add(plan)
        s.commit()
        assert plan.week_number == 1
        assert plan.meals == "Mon: Salad"

def test_meal_plan_invalid_meals(session):
    """Test MealPlan with invalid meals."""
    with session as s:
        user = User(name="Alice")
        s.add(user)
        s.commit()
        plan = MealPlan(user=user, week_number=1, meals="")
        assert plan.meals is None  # Validation prevents setting