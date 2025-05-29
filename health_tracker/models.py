from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import date

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    
    food_entries = relationship("FoodEntry", back_populates="user")
    goals = relationship("Goal", back_populates="user")
    meal_plans = relationship("MealPlan", back_populates="user")
    
    def __init__(self, name):
        self.name = name 

    def get_name(self):
        return self.name
        
    def set_name(self, value):
        if not isinstance(value, str):
            print("Error: Name must be a string!")
            return
        if len(value) < 1:
            print("Error: Name cannot be empty!")
            return
        self.name = value
        
    name = property(get_name, set_name)

class FoodEntry(Base):
    __tablename__ = "food_entries"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    food = Column(String, nullable=False)
    calories = Column(Integer, nullable=False)
    date = Column(Date, nullable=False)
    
    user = relationship("User", back_populates="food_entries")
    
    def __init__(self, user, food, calories, date):
        if not isinstance(user, User):
            print("Error: User must be a User object!")
            return
        if not isinstance(date, date):
            print("Error: Date must be a date object!")
            return
        self.user = user
        self.food = food  
        self.calories = calories  
        self.date = date
        
    def get_food(self):
        return self.food
        
    def set_food(self, value):
        if not isinstance(value, str) or len(value) < 1:
            print("Error: Food must be a non-empty string!")
            return
        self.food = value
        
    food = property(get_food, set_food)
    
    def get_calories(self):
        return self.calories
        
    def set_calories(self, value):
        if not isinstance(value, int) or value <= 0:
            print("Error: Calories must be a positive integer!")
            return
        self.calories = value
        
    calories = property(get_calories, set_calories)

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    daily_calories = Column(Integer, nullable=False)
    weekly_calories = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="goals")
    
    def __init__(self, user, daily_calories, weekly_calories):
        if not isinstance(user, User):
            print("Error: User must be a User object!")
            return
        self.user = user
        self.daily_calories = daily_calori
        self.weekly_calories = weekly_calories  
    
    def get_daily_calories(self):
        return self.daily_calories
        
    def set_daily_calories(self, value):
        if not isinstance(value, int) or value <= 0:
            print("Error: Daily calories must be a positive integer!")
            return
        self.daily_calories = value
        
    daily_calories = property(get_daily_calories, set_daily_calories)
    
    def get_weekly_calories(self):
        return self.weekly_calories
        
    def set_weekly_calories(self, value):
        if not isinstance(value, int) or value <= 0:
            print("Error: Weekly calories must be a positive integer!")
            return
        self.weekly_calories = value
        
    weekly_calories = property(get_weekly_calories, set_weekly_calories)

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    meals = Column(String, nullable=False)
    
    user = relationship("User", back_populates="meal_plans")
    
    def __init__(self, user, week_number, meals):
        if not isinstance(user, User):
            print("Error: User must be a User object!")
            return
        self.user = user
        self.week_number = week_number
        self.meals = meals  
        
    def get_week_number(self):
        return self.week_number
        
    def set_week_number(self, value):
        if not isinstance(value, int) or value <= 0:
            print("Error: Week number must be a positive integer!")
            return
        self.week_number = value
        
    week_number = property(get_week_number, set_week_number)
    
    def get_meals(self):
        return self.meals
        
    def set_meals(self, value):
        if not isinstance(value, str) or len(value) < 1:
            print("Error: Meals must be a non-empty string!")
            return
        self.meals = value
        
    meals = property(get_meals, set_meals)