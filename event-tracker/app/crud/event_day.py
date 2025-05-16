from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.db.models.event import EventDay
from datetime import date

async def create_event_day(db: AsyncSession, event_date: date, name: str) -> EventDay:
    event_day = EventDay(date=event_date, name=name)
    db.add(event_day)
    await db.commit()
    await db.refresh(event_day)
    return event_day

async def list_event_days(db: AsyncSession):
    result = await db.execute(select(EventDay).order_by(EventDay.date))
    return result.scalars().all()
