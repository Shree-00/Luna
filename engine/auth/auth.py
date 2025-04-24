# engine/auth/auth.py
#new
import sqlite3
import hashlib
from engine.auth.session import save_session, load_session, clear_session

DB_PATH = "Luna.db"

def hash_password(password):
    # You could use more robust hashing like bcrypt in production.
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
        user_id = c.lastrowid
        conn.close()
        save_session(user_id)
        return True
    except Exception as e:
        print(f"Signup error: {e}")
        return False

def login(username, password):
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
        result = c.fetchone()
        conn.close()
        if result:
            save_session(result[0])
            return True
        return False
    except Exception as e:
        print(f"Login error: {e}")
        return False

def logout():
    clear_session()

def get_current_user():
    return load_session()
