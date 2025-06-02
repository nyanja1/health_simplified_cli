```python
import typer
from sqlalchemy import select
from sqlalchemy.orm import Session
from health_tracker.database import Session
from health_tracker.models import User, FoodEntry
from datetime import datetime
from typing import Optional

app = typer.Typer(name="myapp", help="Health Simplified CLI for tracking food intake and goals.")

@app.command()
def user_create(name: str):
    """Create a new user with the given name."""
    if not isinstance(name, str) or len(name) < 1:
        typer.echo("Error: Name must be a non-empty string.")
        raise typer.Exit(code=1)
    with Session() as session:
        existing_user = session.execute(select(User).filter_by(name=name)).scalar_one_or_none()
        if existing_user:
            typer.echo(f"Error: User '{name}' already exists.")
            raise typer.Exit(code=1)
        user = User(name=name)
        session.add(user)
        session.commit()
        typer.echo(f"User '{name}' created successfully.")

@app.command()
def user_list():
    """List all users."""
    with Session() as session:
        users = session.execute(select(User)).scalars().all()
        if not users:
            typer.echo("No users found.")
            return
        for user in users:
            typer.echo(f"ID: {user.id}, Name: {user.name}")

@app.command()
def entry_add(user: str, food: str, calories: int, date: str):
    """Add a food entry for a user."""
    if not isinstance(food, str) or len(food) < 1:
        typer.echo("Error: Food must be a non-empty string.")
        raise typer.Exit(code=1)
    if not isinstance(calories, int) or calories <= 0:
        typer.echo("Error: Calories must be a positive integer.")
        raise typer.Exit(code=1)
    try:
        entry_date = datetime.strptime(date, "%Y-%m-%d").date()
    except ValueError:
        typer.echo("Error: Invalid date format. Use YYYY-MM-DD.")
        raise typer.Exit(code=1)
    
    with Session() as session:
        user_obj = session.execute(select(User).filter_by(name=user)).scalar_one_or_none()
        if not user_obj:
            typer.echo(f"Error: User '{user}' not found.")
            raise typer.Exit(code=1)
        
        entry = FoodEntry(
            user=user_obj,
            food=food,
            calories=calories,
            date=entry_date
        )
        session.add(entry)
        session.commit()
        typer.echo(f"Food entry added: {food} ({calories} calories) for {user} on {date}.")

@app.command()
def entry_list(user: Optional[str] = None, date: Optional[str] = None):
    """List food entries, optionally filtered by user or date."""
    with Session() as session:
        query = select(FoodEntry)
        if user:
            user_obj = session.execute(select(User).filter_by(name=user)).scalar_one_or_none()
            if not user_obj:
                typer.echo(f"Error: User '{user}' not found.")
                raise typer.Exit(code=1)
            query = query.filter_by(user_id=user_obj.id)
        if date:
            try:
                entry_date = datetime.strptime(date, "%Y-%m-%d").date()
                query = query.filter_by(date=entry_date)
            except ValueError:
                typer.echo("Error: Invalid date format. Use YYYY-MM-DD.")
                raise typer.Exit(code=1)
        
        entries = session.execute(query).scalars().all()
        if not entries:
            typer.echo("No food entries found.")
            return
        for entry in entries:
            user_name = session.execute(select(User).filter_by(id=entry.user_id)).scalar_one().name
            typer.echo(f"ID: {entry.id}, User: {user_name}, Food: {entry.food}, Calories: {entry.calories}, Date: {entry.date}")

@app.command()
def entry_update(id: int, food: Optional[str] = None, calories: Optional[int] = None, date: Optional[str] = None):
    """Update a food entry by ID."""
    with Session() as session:
        entry = session.execute(select(FoodEntry).filter_by(id=id)).scalar_one_or_none()
        if not entry:
            typer.echo(f"Error: Food entry ID {id} not found.")
            raise typer.Exit(code=1)
        
        if food and (not isinstance(food, str) or len(food) < 1):
            typer.echo("Error: Food must be a non-empty string.")
            raise typer.Exit(code=1)
        if calories is not None and (not isinstance(calories, int) or calories <= 0):
            typer.echo("Error: Calories must be a positive integer.")
            raise typer.Exit(code=1)
        if date:
            try:
                entry_date = datetime.strptime(date, "%Y-%m-%d").date()
                entry.date = entry_date
            except ValueError:
                typer.echo("Error: Invalid date format. Use YYYY-MM-DD.")
                raise typer.Exit(code=1)
        
        if food:
            entry.food = food
        if calories is not None:
            entry.calories = calories
        session.commit()
        typer.echo(f"Food entry ID {id} updated successfully.")

@app.command()
def entry_delete(id: int):
    """Delete a food entry by ID."""
    with Session() as session:
        entry = session.execute(select(FoodEntry).filter_by(id=id)).scalar_one_or_none()
        if not entry:
            typer.echo(f"Error: Food entry ID {id} not found.")
            raise typer.Exit(code=1)
        session.delete(entry)
        session.commit()
        typer.echo(f"Food entry ID {id} deleted successfully.")

if __name__ == "__main__":
    app()
```