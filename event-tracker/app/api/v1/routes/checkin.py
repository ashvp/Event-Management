from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.db.models.attendee import Attendee
from app.crud.checkin import get_or_create_event_day, get_or_create_attendance
from datetime import date
from sqlalchemy.future import select
router = APIRouter()

@router.post("/checkin/")
async def check_in_attendee(name: str = None, email: str = None, phone: str = None, db: AsyncSession = Depends(get_db)):
    query = select(Attendee)
    if email:
        query = query.where(Attendee.email == email)
    elif phone:
        query = query.where(Attendee.phone == phone)
    elif name:
        query = query.where(Attendee.name == name)
    else:
        raise HTTPException(status_code=400, detail="Provide at least one of name, email, or phone")

    result = await db.execute(query)
    attendee = result.scalars().first()

    if not attendee:
        raise HTTPException(status_code=404, detail="Attendee not found. Please register first.")

    today = date.today()
    event_day = await get_or_create_event_day(db, today)
    attendance = await get_or_create_attendance(db, attendee.id, event_day.id)

    return {"message": "Checked in successfully", "attendee_id": attendee.id, "event_day": event_day.date.isoformat()}
