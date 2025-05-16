from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.attendee import AttendeeCreate, AttendeeOut
from app.crud.attendee import create_attendee, get_all_attendees, get_attendee_by_email
from app.db.session import AsyncSessionLocal
import csv
from io import StringIO

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