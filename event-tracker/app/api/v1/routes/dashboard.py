from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.dashboard import get_dashboard_stats
from app.crud.attendee import get_attendees_filtered
from typing import Optional
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

router = APIRouter()

@router.get("/stats/")
async def dashboard_stats(db: AsyncSession = Depends(get_db)):
    return await get_dashboard_stats(db)

@router.get("/")
async def attendees_list(
    search: Optional[str] = Query(None, description="Search by name/email/phone"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    print("🔥 attendees_list was called!")       # <— add this
    print(f"    search parameter is: {search!r}")  # <— and this
    logging.info(f"📥 Received search param: {search!r}") 
    attendees = await get_attendees_filtered(db, search, skip, limit)
    return attendees
