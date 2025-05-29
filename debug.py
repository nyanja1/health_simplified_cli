from health_tracker.database import engine, Session
from health_tracker.models import Base, User, FoodEntry, Goal, MealPlan
from datetime import date

#  tables
Base.metadata.create_all(engine)

#   sessions
session = Session()

#  users
user = User(name="Elvis")
session.add(user)
session.commit()

#  food entries
food_entry = FoodEntry(user=user, food="Pizza", calories=500, date=date(2025, 5, 29))
session.add(food_entry)

#  goals
goal = Goal(user=user, daily_calories=2000, weekly_calories=14000)
session.add(goal)

#  meal plan
meal_plan = MealPlan(user=user, week_number=22, meals="Mon: Salad, Tue: Pasta")
session.add(meal_plan)

session.commit()

# Test properties
print("User:", user.name)
print("Food Entry:", food_entry.food, food_entry.calories)
print("Goal:", goal.daily_calories, goal.weekly_calories)
print("Meal Plan:", meal_plan.week_number, meal_plan.meals)

# Test invalid inputs
user.name = ""  # print error
food_entry.calories = -100  #  print error
goal.daily_calories = "invalid"  #  print error
meal_plan.meals = ""  #  print error

session.close()