```python
import typer
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from health_tracker.database import Session
from health_tracker.models import User, FoodEntry, Goal, MealPlan
from datetime import datetime, date
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

@app.command()
def goal_set(user: str, daily_calories: int, weekly_calories: int):
    """Set or update a user's calorie goals."""
    if not isinstance(daily_calories, int) or daily_calories <= 0:
        typer.echo("Error: Daily calories must be a positive integer.")
        raise typer.Exit(code=1)
    if not isinstance(weekly_calories, int) or weekly_calories <= 0:
        typer.echo("Error: Weekly calories must be a positive integer.")
        raise typer.Exit(code=1)
    
    with Session() as session:
        user_obj = session.execute(select(User).filter_by(name=user)).scalar_one_or_none()
        if not user_obj:
            typer.echo(f"Error: User '{user}' not found.")
            raise typer.Exit(code=1)
        
        existing_goal = session.execute(select(Goal).filter_by(user_id=user_obj.id)).scalar_one_or_none()
        if existing_goal:
            existing_goal.daily_calories = daily_calories
            existing_goal.weekly_calories = weekly_calories
            typer.echo(f"Goal updated for user '{user}'.")
        else:
            goal = Goal(
                user=user_obj,
                daily_calories=daily_calories,
                weekly_calories=weekly_calories
            )
            session.add(goal)
            typer.echo(f"Goal set for user '{user}'.")
        session.commit()

@app.command()
def goal_list(user: Optional[str] = None):
    """List goals, optionally filtered by user."""
    with Session() as session:
        query = select(Goal)
        if user:
            user_obj = session.execute(select(User).filter_by(name=user)).scalar_one_or_none()
            if not user_obj:
                typer.echo(f"Error: User '{user}' not found.")
                raise typer.Exit(code=1)
            query = query.filter_by(user_id=user_obj.id)
        
        goals = session.execute(query).scalars().all()
        if not goals:
            typer.echo("No goals found.")
            return
        for goal in goals:
            user_name = session.execute(select(User).filter_by(id=goal.user_id)).scalar_one().name
            typer.echo(f"ID: {goal.id}, User: {user_name}, Daily Calories: {goal.daily_calories}, Weekly Calories: {goal.weekly_calories}")

@app.command()
def report(user: Optional[str] = None, start_date: Optional[str] = None, end_date: Optional[str] = None):
    """Generate a report of food entries, goals, and meal plans."""
    with Session() as session:
        # Validate dates
        s_date = None
        e_date = None
        if start_date:
            try:
                s_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            except ValueError:
                typer.echo("Error: Invalid start date format. Use YYYY-MM-DD.")
                raise typer.Exit(code=1)
        if end_date:
            try:
                e_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            except ValueError:
                typer.echo("Error: Invalid end date format. Use YYYY-MM-DD.")
                raise typer.Exit(code=1)
        if s_date and e_date and s_date > e_date:
            typer.echo("Error: Start date must be before end date.")
            raise typer.Exit(code=1)

        # Filter by user
        user_obj = None
        if user:
            user_obj = session.execute(select(User).filter_by(name=user)).scalar_one_or_none()
            if not user_obj:
                typer.echo(f"Error: User '{user}' not found.")
                raise typer.Exit(code=1)

        # Food entries
        entry_query = select(FoodEntry)
        if user_obj:
            entry_query = entry_query.filter_by(user_id=user_obj.id)
        if s_date:
            entry_query = entry_query.filter(FoodEntry.date >= s_date)
        if e_date:
            entry_query = entry_query.filter(FoodEntry.date <= e_date)
        
        entries = session.execute(entry_query).scalars().all()
        total_calories = sum(entry.calories for entry in entries)
        
        typer.echo("Report:")
        typer.echo(f"Food Entries ({len(entries)}):")
        for entry in entries:
            typer.echo(f"  - ID: {entry.id}, Food: {entry.food}, Calories: {entry.calories}, Date: {entry.date}")
        typer.echo(f"Total Calories: {total_calories}")

        # Goals
        goal_query = select(Goal)
        if user_obj:
            goal_query = goal_query.filter_by(user_id=user_obj.id)
        goals = session.execute(goal_query).scalars().all()
        typer.echo("Goals:")
        for goal in goals:
            typer.echo(f"  - ID: {goal.id}, Daily: {goal.daily_calories}, Weekly: {goal.weekly_calories}")

        # Meal Plans
        meal_plan_query = select(MealPlan)
        if user_obj:
            meal_plan_query = meal_plan_query.filter_by(user_id=user_obj.id)
        meal_plans = session.execute(meal_plan_query).scalars().all()
        typer.echo("Meal Plans:")
        for plan in meal_plans:
            typer.echo(f"  - Week: {plan.week_number}, Meals: {plan.meals}")

@app.command()
def plan_meal(user: str, week: int, meals: str):
    """Create or update a meal plan for a user and week."""
    if not isinstance(week, int) or week <= 0:
        typer.echo("Error: Week number must be a positive integer.")
        raise typer.Exit(code=1)
    if not isinstance(meals, str) or len(meals) < 1:
        typer.echo("Error: Meals must be a non-empty string.")
        raise typer.Exit(code=1)
    
    with Session() as session:
        user_obj = session.execute(select(User).filter_by(name=user)).scalar_one_or_none()
        if not user_obj:
            typer.echo(f"Error: User '{user}' not found.")
            raise typer.Exit(code=1)
        
        existing_plan = session.execute(
            select(MealPlan).filter_by(user_id=user_obj.id, week_number=week)
        ).scalar_one_or_none()
        if existing_plan:
            existing_plan.meals = meals
            typer.echo(f"Meal plan updated for user '{user}' for week {week}.")
        else:
            plan = MealPlan(
                user=user_obj,
                week_number=week,
                meals=meals
            )
            session.add(plan)
            typer.echo(f"Meal plan created for user '{user}' for week {week}.")
        session.commit()

if __name__ == "__main__":
    app()
```