from fastapi import FastAPI
# from app.db.models.attendee import Attendee
from app.api.v1.routes import attendee, checkin, claim, event_day

app = FastAPI()

app.include_router(attendee.router, prefix="/api/v1/attendees", tags=["attendees"])
app.include_router(checkin.router, prefix="/api/v1", tags=["checkin"])
app.include_router(claim.router, prefix="/api/v1", tags=["claim"])
app.include_router(event_day.router, prefix="/api/v1", tags=["event_days"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Event Tracker API!"}