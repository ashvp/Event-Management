# 🎪 RFID Event Management System

A blazing-fast 🏃‍♂️, offline-first 📴, and scalable ⚡ backend for managing attendees, check-ins, wristbands, and more — all powered by **FastAPI + PostgreSQL + RFID**.

---

## 🚀 Features

* 🎟️ **Attendee Onboarding via CSV & UI**
* 🚂 **RFID Wristband Assignment**
* ⏱️ **Real-time Check-in/Check-out Tracking**
* 🡾 **Freebies & Kit Distribution Tracking**
* 🔌 **Offline Caching for Desks**
* 🔄 **Multi-System Syncing with Conflict Resolution**
* 🔒 **Data Integrity & Deduplication**

---

## 🧠 Tech Stack

| Layer          | Tech                             |
| -------------- | -------------------------------- |
| Backend API    | ⚡ FastAPI                        |
| Database       | 🐘 PostgreSQL + SQLite (Offline) |
| RFID Interface | 🎯 PySerial / Device SDK         |
| Caching        | 📦 Local JSON / SQLite           |
| Deployment     | ☁️ Docker-ready                  |

---

## 🛠️ Setup Instructions

### 1. Clone the repo

```bash
git clone https://github.com/your-org/rfid-event-backend.git
cd rfid-event-backend
```

### 2. Install dependencies

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup PostgreSQL

Create a `.env` file with your DB creds:

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/rfid_event
```

Run migrations:

```bash
alembic upgrade head
```

### 4. Run the backend

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Testing

```bash
pytest
```

---

## 📆 API Endpoints

```http
POST   /attendees/           → Bulk onboard via CSV
GET    /attendees/{id}       → Get attendee info
POST   /check-in/            → Record a check-in
POST   /assign-rfid/         → Bind RFID tag
GET    /sync/unsynced        → View unsynced records (offline desks)
POST   /sync/merge           → Push offline records to central
```

📚 Full docs available at `/docs` via Swagger UI.

---

## 🤝 Contributing

Wanna help out? Pull requests welcome!
Please follow the [conventional commits](https://www.conventionalcommits.org/) style and keep PRs atomic.

---

## 🚇 Known Challenges

* RFID reader behavior can vary by vendor 🤷‍♂️
* Offline-first mode can cause timestamp conflicts — we dedupe based on `uuid + ts`
* SQLite schema must match production schema — auto-migration WIP 🔧

---

## 📊 Roadmap

* [ ] Admin Dashboard (Streamlit / Vue)
* [ ] PDF Badge Generator
* [ ] Realtime WebSocket Sync
* [ ] Telegram Bot for Check-in Alerts 📲

---

## 🐛 Bug? Suggestion?

Open an issue or hit us up via carrier pigeon.
Seriously, just open an issue ☛ [here](https://github.com/your-org/rfid-event-backend/issues)

---

## 📜 License

MIT © Your Team Name 2025

---

## 💡 Fun Fact

Each wristband is basically a tiny dumb storage device with a superpower: being at the right place at the right time.

---
