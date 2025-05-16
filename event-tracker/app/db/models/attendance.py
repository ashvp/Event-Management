from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.db.base import Base

class Attendance(Base):
    __tablename__ = "attendances"
    id = Column(Integer, primary_key=True, index=True)
    attendee_id = Column(Integer, ForeignKey("attendees.id"), nullable=False)
    event_day_id = Column(Integer, ForeignKey("event_days.id"), nullable=False)
    checked_in = Column(Boolean, default=False)
    got_kit = Column(Boolean, default=False)
    got_lunch = Column(Boolean, default=False)
    got_freebies = Column(Boolean, default=False)

    attendee = relationship("Attendee", back_populates="attendances")
    event_day = relationship("EventDay", back_populates="attendances")
