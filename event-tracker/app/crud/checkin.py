from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from app.db.models.attendee import Attendee
from app.db.models.event import EventDay
from app.db.models.attendance import Attendance
from datetime import date

async def get_or_create_event_day(db: AsyncSession, day: date) -> EventDay:
    result = await db.execute(select(EventDay).where(EventDay.date == day))
    event_day = result.scalars().first()
    if event_day:
        return event_day

    event_day = EventDay(date=day, name=f"Day {day.isoformat()}")
    db.add(event_day)
    await db.commit()
    await db.refresh(event_day)
    return event_day

async def get_or_create_attendance(db: AsyncSession, attendee_id: int, event_day_id: int) -> Attendance:
    result = await db.execute(
        select(Attendance).where(
            Attendance.attendee_id == attendee_id,
            Attendance.event_day_id == event_day_id
        )
    )
    attendance = result.scalars().first()
    if attendance:
        return attendance

    attendance = Attendance(
        attendee_id=attendee_id,
        event_day_id=event_day_id,
        checked_in=True
    )
    db.add(attendance)
    await db.commit()
    await db.refresh(attendance)
    return attendance
