# app/crud/claim.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.attendee import Attendee
from app.db.models.event import EventDay
from app.db.models.attendance import Attendance
from datetime import date

async def claim_item(db: AsyncSession, rfid_uid: str, item: str):
    # Step 1: Fetch attendee by RFID
    result = await db.execute(select(Attendee).where(Attendee.rfid_uid == rfid_uid))
    attendee = result.scalars().first()
    if not attendee:
        return {"status": "error", "detail": "RFID not registered"}

    # Step 2: Get today's event day
    today = date.today()
    result = await db.execute(select(EventDay).where(EventDay.date == today))
    event_day = result.scalars().first()
    if not event_day:
        return {"status": "error", "detail": "Event day not initialized"}

    # Step 3: Get today's attendance
    result = await db.execute(
        select(Attendance).where(
            Attendance.attendee_id == attendee.id,
            Attendance.event_day_id == event_day.id
        )
    )
    attendance = result.scalars().first()
    if not attendance:
        return {"status": "error", "detail": "Attendee not checked in today"}

    # Step 4: Check if item already claimed
    if getattr(attendance, item):
        return {"status": "denied", "detail": f"{item.replace('_', ' ').title()} already claimed"}

    # Step 5: Mark as claimed
    setattr(attendance, item, True)
    db.add(attendance)
    await db.commit()
    return {"status": "success", "message": f"{item.replace('_', ' ').title()} claimed successfully"}
