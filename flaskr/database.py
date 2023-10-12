from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_NAME = 'projectdb'

engine = create_engine(f'postgresql:///{DATABASE_NAME}')
session = sessionmaker(bind=engine)

Base = declarative_base()


def create_db():
    passf




    # database="projectdb",
    # host="localhost",
    # user="projectdb",
    # password="projectdb",
    # port="5432")