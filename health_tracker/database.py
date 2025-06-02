```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Create SQLite database
engine = create_engine("sqlite:///health.db")
Session = sessionmaker(bind=engine)

# Create tables
Base.metadata.create_all(engine)
```