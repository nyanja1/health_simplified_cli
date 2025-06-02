```python
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from health_tracker.models import Base, User, FoodEntry
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
```