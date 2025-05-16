from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from app.db.models.attendee import Attendee
from app.api.v1.routes import attendee, checkin, claim, event_day, dashboard
import logging
from app.utils.offline_queue import start_sync_thread

app = FastAPI()

origins = [
    "http://localhost:3000",
    # add other origins if you want
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
logging.getLogger("sqlalchemy.engine").setLevel(logging.DEBUG)

app.include_router(attendee.router, prefix="/api/v1/attendees", tags=["attendees"])
app.include_router(checkin.router, prefix="/api/v1", tags=["checkin"])
app.include_router(claim.router, prefix="/api/v1", tags=["claim"])
app.include_router(event_day.router, prefix="/api/v1", tags=["event_days"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["dashboard"])

@app.on_event("startup")
async def startup_event():
    start_sync_thread()

@app.get("/")
async def root():
    return {"message": "Welcome to the Event Tracker API!"}