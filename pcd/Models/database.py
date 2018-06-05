from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

Engine = create_engine('sqlite:///:memory:')


class Database:
    __database = None
    engine = Engine
    Session = sessionmaker(bind=engine)
    session = Session()
    Base = declarative_base()

    def __new__(cls):
        if Database.__database is None:
            Database.__database = object.__new__(cls)
        return Database.__database


data = Database()
