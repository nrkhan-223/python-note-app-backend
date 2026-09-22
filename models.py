from sqlalchemy import Column, Integer, String, true
from database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True,unique=True)
    content = Column(String)
