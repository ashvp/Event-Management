from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from app.db.models.attendee import Attendee
from app.schemas.attendee import AttendeeCreate
from typing import Optional
import logging

logger = logging.getLogger(__name__)

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

async def assign_rfid_to_attendee(db: AsyncSession, attendee_id: int, rfid_uid: str):
    result = await db.execute(select(Attendee).where(Attendee.rfid_uid == rfid_uid))
    existing = result.scalar_one_or_none()
    if existing:
        raise ValueError("RFID UID is already assigned to another attendee.")

    result = await db.execute(select(Attendee).where(Attendee.id == attendee_id))
    attendee = result.scalar_one_or_none()
    if not attendee:
        raise ValueError("Attendee not found.")

    attendee.rfid_uid = rfid_uid
    attendee.registered = True  
    await db.commit()
    await db.refresh(attendee)
    return attendee

async def get_attendees_filtered(
    db: AsyncSession,
    search: Optional[str] = None,
    skip: int = 0,
    limit: int = 20,
):

    stmt = select(Attendee)

    if search and search.strip():
        term = f"%{search.strip()}%"
        stmt = stmt.where(
            or_(
                Attendee.name.ilike(term),
                Attendee.email.ilike(term),
                Attendee.phone.ilike(term),
            )
        )

    stmt = stmt.order_by(Attendee.name).offset(skip).limit(limit)

    result = await db.execute(stmt)
    rows = result.scalars().all()
    return rows
