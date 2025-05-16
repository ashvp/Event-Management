# app/crud/dashboard.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.db.models.attendee import Attendee
from app.db.models.attendance import Attendance

async def get_dashboard_stats(db: AsyncSession):
    total_registered = await db.scalar(select(func.count()).select_from(Attendee))
    
    total_checked_in = await db.scalar(
        select(func.count()).select_from(Attendance).where(Attendance.checked_in == True)
    )
    
    total_kits = await db.scalar(
        select(func.count()).select_from(Attendance).where(Attendance.got_kit == True)
    )
    
    total_lunches = await db.scalar(
        select(func.count()).select_from(Attendee).where(Attendee.got_lunch == True)
    )
    
    total_freebies = await db.scalar(
        select(func.count()).select_from(Attendance).where(Attendance.got_freebies == True)
    )
    
    return {
        "total_registered": total_registered,
        "total_checked_in": total_checked_in,
        "total_kits": total_kits,
        "total_lunches": total_lunches,
        "total_freebies": total_freebies,
    }
