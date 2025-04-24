# engine/auth/session.py
#new
import json
from pathlib import Path

SESSION_FILE = Path("engine/.session")

def save_session(user_id):
    with open(SESSION_FILE, 'w') as f:
        json.dump({"user_id": user_id}, f)

def load_session():
    if not SESSION_FILE.exists():
        return None
    with open(SESSION_FILE) as f:
        data = json.load(f)
        return data.get("user_id")

def clear_session():
    if SESSION_FILE.exists():
        SESSION_FILE.unlink()

def is_logged_in():
    return SESSION_FILE.exists()
