
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
            print("Name must be a string!")
            return
        if len(value) < 1:
            print(" Name cannot be empty!")
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

class Goal(Base):
    __tablename__ = "goals"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    daily_calories = Column(Integer, nullable=False)
    weekly_calories = Column(Integer, nullable=False)
    
    user = relationship("User", back_populates="goals")
    
    def __init__(self, user, daily_calories, weekly_calories):
        self.user = user
        self.daily_calories = daily_calories
        self.weekly_calories = weekly_calories

class MealPlan(Base):
    __tablename__ = "meal_plans"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    week_number = Column(Integer, nullable=False)
    meals = Column(String, nullable=False)  # Simple string for meals
    
    user = relationship("User", back_populates="meal_plans")
    
    def __init__(self, user, week_number, meals):
        self.user = user
        self.week_number = week_number
        self.meals = meals