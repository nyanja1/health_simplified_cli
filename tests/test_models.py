import pytest
from health_tracker.models import User

def test_user_creation():
    user = User(name="Elvis")
    assert user.name == "Elvis"