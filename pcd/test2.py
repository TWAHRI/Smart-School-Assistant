import Models.Models_classes as Mo
from sqlalchemy import Table, String, Integer, ForeignKey, Column, Date
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import datetime
import os


name = 123
# os.mkdir("/home/amani/Documents/pcd/Data/Schedules/"+str(name))
schedule_path = "/home/amani/Documents/pcd/Data/Schedules/" + os.listdir("/home/amani/Documents/pcd/Data/Schedules/"+str(name))[0]
print(schedule)
