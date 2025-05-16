# app/api/v1/routes/claim.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.crud.claim import claim_item
from pydantic import BaseModel

router = APIRouter()

class RFIDPayload(BaseModel):
    rfid_uid: str

@router.post("/claim/{item_name}")
async def claim_event_item(item_name: str, payload: RFIDPayload, db: AsyncSession = Depends(get_db)):
    valid_items = ["got_kit", "got_lunch", "got_freebies"]
    if item_name not in valid_items:
        raise HTTPException(status_code=400, detail="Invalid claim type")

    result = await claim_item(db, payload.rfid_uid, item_name)
    if result["status"] == "error":
        raise HTTPException(status_code=404, detail=result["detail"])
    if result["status"] == "denied":
        raise HTTPException(status_code=409, detail=result["detail"])

    return {"message": result["message"]}
