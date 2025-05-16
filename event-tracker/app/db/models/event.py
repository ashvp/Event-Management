from sqlalchemy import Column, Integer, Date, String
from sqlalchemy.orm import relationship
from app.db.base import Base

class EventDay(Base):
    __tablename__ = "event_days"
    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, unique=True, index=True)
    name = Column(String, nullable=True)  # e.g. "Day 1", "Opening Day"
    
    # Relationships
    attendances = relationship("Attendance", back_populates="event_day")
