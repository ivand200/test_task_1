from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


# SQLALCHEMY_DATABASE_URL = (
#     f"postgresql://lbdqzbcw:p_P9s4_3yh_N-8e-gnvUwQIGIpemIUML@abul.db.elephantsql.com/lbdqzbcw"
# )

SQLALCHEMY_DATABASE_URL = (
    f"sqlite:///./db.db"
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()