from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create SQLite database
engine = create_engine("sqlite:///health.db")

Session = sessionmaker(bind=engine)