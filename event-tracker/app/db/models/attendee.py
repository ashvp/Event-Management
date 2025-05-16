from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base, relationship
from app.db.base import Base
import enum

# Base = declarative_base()

class RoleEnum(str, enum.Enum):
    attendee = "Attendee"
    speaker = "Speaker"
    organizer = "Organizer"

class Attendee(Base):
    __tablename__ = "attendees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.attendee)

    rfid_uid = Column(String, unique=True, nullable=True)  # Can be null before assignment

    registered = Column(Boolean, default=False)
    got_kit = Column(Boolean, default=False)
    got_lunch = Column(Boolean, default=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    attendances = relationship("Attendance", back_populates="attendee")
