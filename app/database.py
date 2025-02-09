from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from app.config import DATABASE_URL

# Debugging: Print DATABASE_URL to ensure it's correct
print(f"🔍 DATABASE_URL: {DATABASE_URL}")

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    connection = engine.connect()
    print("✅ Successfully connected to PostgreSQL!")
    connection.close()
except Exception as e:
    print(f"❌ Database connection error: {e}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
