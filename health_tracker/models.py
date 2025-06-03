
from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, declarative_base
from datetime import date

Base = declarative_base()

class User(Base):
    """Represents a user in the health tracking system."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    food_entries = relationship("FoodEntry", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    meal_plans = relationship("MealPlan", back_populates="user")

    def __init__(self, name):
        """Initialize a User with a name.

        Args:
            name (str): The user's name.

        Returns:
            None: If name is invalid, prints error and returns.
        """
        if not isinstance(name, str) or len(name.strip()) == 0:
            print("Error: Name must be a non-empty string")
            return
        self.name = name.strip()

    @property
    def name(self):
        """Get the user's name."""
        return self._name
    
    @name.setter
    def name(self, value):
        """Set the user's name.

        Args:
            value (str): The new name.

        Returns:
            None: If value is invalid, prints error and returns.
        """
        if not isinstance(value, str) or len(value.strip()) == 0:
            print("Error: Name must be a non-empty string")
            return
        self._name = value.strip()

class FoodEntry(Base):
    """Represents a food entry for a user."""
    __tablename__ = "food_entries"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    
    user = relationship("User", back_populates="food_entries")

    def __init__(self, user, food, calories, date):
        """Initialize a FoodEntry.

        Args:
            user (User): The associated user.
            food (str): The food item.
            calories (int): Calorie count.
            date (date): Date of entry.

        Returns:
            None: If inputs are invalid, prints error and returns.
        """
        if not isinstance(food, str) or len(food.strip()) == 0:
            print("Error: Food must be a non-empty string")
            return
        if not isinstance(calories, int) or calories <= 0:
            print("Error: Calories must be a positive integer")
            return
        if not isinstance(date, date):
            print("Error: Date must be a valid date")
            return
        self.user = user
        self.food = food.strip()
        self.calories = calories
        self.date = date

    @property
    def calories(self):
        """Get the calorie count."""
        return self._calories
    
    @calories.setter
    def calories(self, value):
        """Set the calorie count.

        Args:
            value (int): The new calorie count.

        Returns:
            None: If value is invalid, prints error and returns.
        """
        if not isinstance(value, int) or value <= 0:
            print("Error: Calories must be a positive integer")
            return
        self._calories = value

class Goal(Base):
    """Represents a user's calorie goals."""
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    daily_calories = Column(Integer, nullable=False)
    weekly_calories = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="goals")

    def __init__(self, user, daily_calories, weekly_calories):
        """Initialize a Goal.

        Args:
            user (User): The associated user.
            daily_calories (int): Daily calorie goal.
            weekly_calories (int): Weekly calorie goal.

        Returns:
            None: If inputs are invalid, prints error and returns.
        """
        if not isinstance(daily_calories, int) or daily_calories <= 0:
            print("Error: Daily calories must be a positive integer")
            return
        if not isinstance(weekly_calories, int) or weekly_calories <= 0:
            print("Error: Weekly calories must be a positive integer")
            return
        self.user = user
        self.daily_calories = daily_calories
        self.weekly_calories = weekly_calories

    @property
    def daily_calories(self):
        """Get the daily calorie goal."""
        return self._daily_calories
    
    @daily_calories.setter
    def daily_calories(self, value):
        """Set the daily calorie goal.

        Args:
            value (int): The new daily calorie goal.

        Returns:
            None: If value is invalid, prints error and returns.
        """
        if not isinstance(value, int) or value <= 0:
            print("Error: Daily calories must be a positive integer")
            return
        self._daily_calories = value

class MealPlan(Base):
    """Represents a user's meal plan for a week."""
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    meals = Column(String, nullable=False)
    
    user = relationship("User", back_populates="meal_plans")

    def __init__(self, user, week_number, meals):
        """Initialize a MealPlan.

        Args:
            user (User): The associated user.
            week_number (int): Week number.
            meals (str): Meal plan details.

        Returns:
            None: If inputs are invalid, prints error and returns.
        """
        if not isinstance(week_number, int) or week_number <= 0:
            print("Error: Week number must be a positive integer")
            return
        if not isinstance(meals, str) or len(meals.strip()) == 0:
            print("Error: Meals must be a non-empty string")
            return
        self.user = user
        self.week_number = week_number
        self.meals = meals.strip()

    @property
    def meals(self):
        """Get the meal plan details."""
        return self._meals
    
    @meals.setter
    def meals(self, value):
        """Set the meal plan details.

        Args:
            value (str): The new meal plan details.

        Returns:
            None: If value is invalid, prints error and returns.
        """
        if not isinstance(value, str) or len(value.strip()) == 0:
            print("Error: Meals must be a non-empty string")
            return
        self._meals = value.strip(