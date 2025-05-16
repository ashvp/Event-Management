from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from app.db.models.attendee import Attendee
from app.schemas.attendee import AttendeeCreate
from typing import Optional

async def create_attendee(db: AsyncSession, attendee: AttendeeCreate) -> Attendee:
    db_attendee = Attendee(**attendee.dict())
    db.add(db_attendee)
    try:
        await db.commit()
        await db.refresh(db_attendee)
    except IntegrityError:
        await db.rollback()
        raise ValueError("Attendee with this email already exists.")
    return db_attendee

async def get_attendee_by_email(db: AsyncSession, email: str) -> Optional[Attendee]:
    result = await db.execute(select(Attendee).where(Attendee.email == email))
    return result.scalars().first()

async def get_all_attendees(db: AsyncSession) -> list[Attendee]:
    result = await db.execute(select(Attendee))
    return result.scalars().all()
