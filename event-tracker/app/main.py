from fastapi import FastAPI
from app.db.models.attendee import Attendee
from app.api.v1.routes import attendee

app = FastAPI()

app.include_router(attendee.router, prefix="/api/v1/attendees", tags=["attendees"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Event Tracker API!"}