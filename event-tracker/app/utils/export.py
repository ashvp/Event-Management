import csv
import os
from datetime import datetime
from sqlalchemy import select
from app.db.models.attendee import Attendee
from sqlalchemy.ext.asyncio import AsyncSession

EXPORT_DIR = "exports"

async def export_rfid_assignments(db: AsyncSession):
    os.makedirs(EXPORT_DIR, exist_ok=True)
    
    date_str = datetime.utcnow().strftime("%Y-%m-%d")
    filename = f"rfid_assignments_{date_str}.csv"
    path = os.path.join(EXPORT_DIR, filename)

    result = await db.execute(select(Attendee).where(Attendee.rfid_uid.isnot(None)))
    attendees = result.scalars().all()

    with open(path, mode="w", newline='', encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Email", "Phone", "Role", "RFID_UID", "Registered", "RFID_Assigned_At"])
        for a in attendees:
            timestamp = a.updated_at.isoformat() if hasattr(a, "updated_at") else ""
            writer.writerow([a.name, a.email, a.phone, a.role, a.rfid_uid, a.registered, timestamp])
