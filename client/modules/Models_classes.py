from sqlalchemy import Table, String, Integer, ForeignKey, Column, Date, select, inspect, MetaData, update
from sqlalchemy.orm import relationship, sessionmaker, backref, joinedload, lazyload
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime

Engine = create_engine('sqlite:////tmp/test.db')


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

association_reu_prof = Table('association_reu_prof', data.Base.metadata,
                             Column('person_id', Integer, ForeignKey('professor.person_id', onupdate="CASCADE", ondelete="CASCADE")),
                             Column('reunion_id', Integer, ForeignKey('reunion.reunion_id', onupdate="CASCADE", ondelete="CASCADE"))
                             )

association_class_prof = Table('association_class_prof', data.Base.metadata,
                               Column('person_id', Integer, ForeignKey('professor.person_id', onupdate="CASCADE", ondelete="CASCADE")),
                               Column('class_id', Integer, ForeignKey('class.class_id', onupdate="CASCADE", ondelete="CASCADE"))
                               )


class Person (data.Base):
    __tablename__ = 'person'

    person_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    CIN = Column(Integer)
    num_tel = Column(Integer)
    photo_folder_path = Column(String(200))
    discriminator = Column('type', String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}


class Professor(Person):
    __tablename__ = 'professor'

    __mapper_args__ = {'polymorphic_identity': 'professor'}
    person_id = Column(Integer, ForeignKey('person.person_id'), primary_key=True)
    emploi_path = Column(String(200))
    reunions = relationship(
        "Reunion",
        secondary=association_reu_prof,
        backref=backref("professors"), lazy='joined')
    classes = relationship(
        "Class",
        secondary=association_class_prof,
        backref=backref("professors"), lazy='joined')

    def __repr__(self):
        return "<professor(id='%d', name='%s', CIN='%d', num_tel='%s', photo_folder_path='%s', emploi_path='%s')>" % (
            self.person_id, self.name, self.CIN, self.num_tel, self.photo_folder_path, self.emploi_path)


class Event(data.Base):
    __tablename__ = 'event'

    event_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    date = Column(Date)

    def __repr__(self):
        return"<event(name='%s')>" % (self.name)


class Reunion(data.Base):
    __tablename__ = 'reunion'

    reunion_id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    date = Column(Date)

    def __repr__(self):
        return"<reunion(name='%s')>" % (self.name)


class Student(Person):
    __tablename__ = 'student'

    __mapper_args__ = {'polymorphic_identity': 'student'}
    person_id = Column(Integer, ForeignKey('person.person_id'), primary_key=True)
    class_id = Column(Integer, ForeignKey('class.class_id', onupdate="CASCADE", ondelete="CASCADE"))
    _class = relationship("Class", back_populates="students", lazy='joined')

    def __repr__(self):
        return "<student(id='%d' ,name='%s', CIN='%d', num_tel='%s', photo_folder_path='%s')>" % (
            self.person_id, self.name, self.CIN, self.num_tel, self.photo_folder_path)


class Class(data.Base):
    __tablename__ = 'class'

    class_id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)
    emploi_path = Column(String(200))
    students = relationship("Student", back_populates="_class", lazy='joined')
    results = relationship("Result", back_populates="_class", lazy='joined')
    def __repr__(self):
        return "<Class(id='%d' ,name='%s', emploi_path='%s')>" % (
            self.class_id, self.name, self.emploi_path)


class Result(data.Base):
    __tablename__ = 'result'
    results_id = Column(Integer, primary_key=True)
    result_folder_path = Column(String(200))
    date = Column(Date)
    class_id = Column(Integer, ForeignKey('class.class_id', onupdate="CASCADE"))
    _class = relationship("Class", back_populates="results", lazy='joined')

# data.Base.metadata.drop_all(data.engine)
data.Base.metadata.create_all(data.engine)
