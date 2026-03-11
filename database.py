from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine



db_url = "postgresql://postgres:Qwerty123@localhost:5432/CRUD"
engine = create_engine(db_url)
session = sessionmaker(autocommit = False,autoflush=False,bind=engine)