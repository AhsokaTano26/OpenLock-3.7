from sqlalchemy import Column, Integer, String, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'User'
    User_name = Column(String(100), primary_key=True)
    full_name = Column(String(100), nullable=False)
    SPT = Column(Integer, default=0)
    DRSG = Column(Integer, default=0)
    FIS = Column(Integer, default=0)
    UV = Column(Integer, default=0)
    TRA = Column(Integer, default=0)
    AG = Column(Integer, default=0)
    COMF = Column(Integer, default=0)
    FLU = Column(Integer, default=0)
    AP = Column(Integer, default=0)
    AC = Column(Integer, default=0)
    GL = Column(Integer, default=0)
    MU = Column(Integer, default=0)
    DC = Column(Integer, default=0)
    PTFC = Column(Integer, default=0)
    SPI = Column(Integer, default=0)
    CW = Column(Integer, default=0)
    if_come_late = Column(Integer, default=0)
    relationship = Column(String(200))  #admin/family/friend/neighbor
    mailbox = Column(String(200))
    if_like_moonPhase = Column(Integer, default=0)
    update_time = Column(String(200), default=datetime.datetime.now)

class WeatherDisaster(Base):
    __tablename__ = 'WeatherDisaster'
    id = Column(String(200), primary_key=True, nullable=False)