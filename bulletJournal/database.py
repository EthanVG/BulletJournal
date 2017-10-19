from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey, DateTime, Date

from . import app

engine = create_engine(app.config["DATABASE_URI"])
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
        
class Bullet(Base):
    __tablename__ = 'bullets'
    
    id = Column(Integer, primary_key=True)
    contentType = Column(String(128), nullable=False)
    content = Column(String(128), nullable=False)
    date = Column(Date, nullable=False)

Base.metadata.create_all(engine)