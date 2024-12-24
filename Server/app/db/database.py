from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database URL: Replace with your credentials
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Imad2002@localhost:5432/IA1"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our models it help us to create the tables
Base = declarative_base()
#useful for the route it help us to interact with the database

def get_db():
    db = SessionLocal()
    try:
        yield db # it create more session
    finally:
        db.close() #close the instance
