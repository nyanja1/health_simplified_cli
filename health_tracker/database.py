from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# SQLite database
engine = create_engine("sqlite:///health.db")

# session factory
Session = sessionmaker(bind=engine)