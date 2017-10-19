from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean
from sqlalchemy.orm import relationship
from .database import session

from .database import Base
        
class Bullet(Base):
    __tablename__ = 'bullets'
    
    id = Column(Integer, primary_key=True)
    contentType = Column(String(128), nullable=False)
    content = Column(String(128), nullable=False)
    #completed = Column(Boolean, nullable=False)
    
    