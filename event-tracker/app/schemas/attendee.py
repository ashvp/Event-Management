from pydantic import BaseModel, EmailStr
from typing import Optional
from enum import Enum

class RoleEnum(str, Enum):
    attendee = "Attendee"
    speaker = "Speaker"
    organizer = "Organizer"

class AttendeeBase(BaseModel):
    name: str
    email: EmailStr
    phone: str
    role: RoleEnum

class AttendeeCreate(AttendeeBase):
    pass

class AttendeeOut(AttendeeBase):
    id: int
    rfid_uid: Optional[str]
    registered: bool
    got_kit: bool
    got_lunch: bool

    model_config = {
        "from_attributes": True
    }

class RFIDAssign(BaseModel):
    rfid_uid: str
