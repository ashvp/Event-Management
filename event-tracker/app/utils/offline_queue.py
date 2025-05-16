# app/utils/offline_queue.py

import sqlite3
import threading
import time
import requests
import json

DB_PATH = "sync_queue.db"
SYNC_INTERVAL = 10  # seconds

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS queue (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                url TEXT NOT NULL,
                method TEXT NOT NULL,
                payload TEXT,
                headers TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)

def queue_action(url: str, method: str, payload: dict = None, headers: dict = None):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            "INSERT INTO queue (url, method, payload, headers) VALUES (?, ?, ?, ?)",
            (url, method.upper(), json.dumps(payload or {}), json.dumps(headers or {}))
        )

def process_queue():
    while True:
        try:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.execute("SELECT id, url, method, payload, headers FROM queue ORDER BY id")
                rows = cursor.fetchall()

                for row in rows:
                    qid, url, method, payload, headers = row
                    try:
                        response = requests.request(
                            method=method,
                            url=url,
                            headers=json.loads(headers),
                            json=json.loads(payload),
                            timeout=5
                        )
                        if response.status_code < 400:
                            conn.execute("DELETE FROM queue WHERE id = ?", (qid,))
                    except Exception as e:
                        print(f"[SYNC] Failed for {url}: {e}")

        except Exception as outer:
            print(f"[SYNC] Queue processing error: {outer}")

        time.sleep(SYNC_INTERVAL)

def start_sync_thread():
    init_db()
    thread = threading.Thread(target=process_queue, daemon=True)
    thread.start()
