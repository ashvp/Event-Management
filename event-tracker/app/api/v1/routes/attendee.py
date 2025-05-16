from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.attendee import AttendeeCreate, AttendeeOut, RFIDAssign
from app.crud.attendee import create_attendee, get_all_attendees, get_attendee_by_email, assign_rfid_to_attendee
from app.db.session import AsyncSessionLocal
from app.utils.export import export_rfid_assignments
from fastapi.responses import FileResponse

import csv
import os
from io import StringIO
from datetime import datetime

router = APIRouter()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

@router.post("/", response_model=AttendeeOut)
async def add_attendee(attendee: AttendeeCreate, db: AsyncSession = Depends(get_db)):
    return await create_attendee(db, attendee)

@router.get("/", response_model=list[AttendeeOut])
async def list_attendees(db: AsyncSession = Depends(get_db)):
    return await get_all_attendees(db)

@router.post("/upload_csv")
async def upload_attendees_csv(file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    content = await file.read()
    decoded = content.decode("utf-8")
    reader = csv.DictReader(StringIO(decoded))

    created = 0
    skipped = 0
    for row in reader:
        email = row.get("Email")
        existing = await get_attendee_by_email(db, email)
        if existing:
            skipped += 1
            continue

        try:
            attendee_data = AttendeeCreate(
                name=row["Name"],
                email=email,
                phone=row["Phone"],
                role=row["Role"].capitalize()
            )
            await create_attendee(db, attendee_data)
            created += 1
        except Exception as e:
            skipped += 1  # can log error here

    return {
        "created": created,
        "skipped": skipped
    }

@router.post("/{attendee_id}/assign_rfid")
async def assign_rfid(attendee_id: int, payload: RFIDAssign, db: AsyncSession = Depends(get_db)):
    try:
        attendee = await assign_rfid_to_attendee(db, attendee_id, payload.rfid_uid)
        await export_rfid_assignments(db)  # <-- this auto-updates the CSV
        return {"message": "RFID assigned successfully", "attendee": attendee}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@router.get("/rfid_export/")
async def download_rfid_export(date: str = Query(default=None, description="Date in YYYY-MM-DD")):
    # if no date provided, default to today
    date_obj = datetime.utcnow()
    if date:
        try:
            date_obj = datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    filename = f"rfid_assignments_{date_obj.strftime('%Y-%m-%d')}.csv"
    filepath = os.path.join("exports", filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Export file not found for the given date.")

    return FileResponse(filepath, media_type="text/csv", filename=filename)