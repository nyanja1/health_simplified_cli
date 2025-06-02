import pytest
from health_tracker.models import User, FoodEntry
from datetime import date

def test_user_creation():
    user = User(name="Elvis")
    assert user.name == "Elvis"

def test_food_entry_creation():
    user = User(name="Elvis")
    entry = FoodEntry(user=user, food="Pizza", calories=500, date=date(2025, 5, 29))
    assert entry.food == "Pizza"
    assert entry.calories == 500