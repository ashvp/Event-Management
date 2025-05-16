from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.event_day import create_event_day, list_event_days
from pydantic import BaseModel
from datetime import date

router = APIRouter()

class EventDayCreate(BaseModel):
    date: date
    name: str

@router.post("/event_day/")
async def create_day(payload: EventDayCreate, db: AsyncSession = Depends(get_db)):
    day = await create_event_day(db, payload.date, payload.name)
    return {"message": "Event day created", "id": day.id, "date": str(day.date)}

@router.get("/event_day/")
async def get_days(db: AsyncSession = Depends(get_db)):
    days = await list_event_days(db)
    return days
