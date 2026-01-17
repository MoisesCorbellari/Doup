from sqlalchemy import Column, Date, Integer, String, Boolean, Text
from shared.database import Base
from datetime import date

class DoUp(Base):
    __tablename__ = "DoUp"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False) 
    description = Column(Text, nullable=True) 
    created = Column(Date, nullable=False, default=date.today)
    completed = Column(Boolean, nullable=False, default=False)
