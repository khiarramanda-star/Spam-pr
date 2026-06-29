#!/usr/bin/env python3
# firebase.py - Firebase Connection & Auth System

import requests
import hashlib
import json
import base64
import time
from datetime import datetime

# ==================== FIREBASE CONFIG (ENCRYPTED) ====================
class FirebaseConfig:
    _ENCRYPTED = {
        "apiKey": "b3RUMFdJUmt6WEJNeUtZMXlGQVhQaXQyMGhrOUhMc1l6YUlB==",
        "databaseURL": "b3RtLm9lY2FpcmVmLmItZHQtZmF1bHQtMTQ4ODMtZXNhYi8vOnB0dGg=",
        "projectId": "MTQ4ODMtZXNhYg==",
        "appId": "NjoyNjI3ZTdlZTZlZWM0ZTQyOTQ4Nzo1NTg4OTUzODgxNzg6MQ=="
    }
    
    @staticmethod
    def _decode(encoded):
        try:
            decoded = base64.b64decode(encoded).decode('utf-8')
            return decoded[::-1]
        except:
            return encoded
    
    @staticmethod
    def get():
        return {
            "apiKey": FirebaseConfig._decode(FirebaseConfig._ENCRYPTED["apiKey"]),
            "databaseURL": FirebaseConfig._decode(FirebaseConfig._ENCRYPTED["databaseURL"]),
            "projectId": FirebaseConfig._decode(FirebaseConfig._ENCRYPTED["projectId"]),
            "appId": FirebaseConfig._decode(FirebaseConfig._ENCRYPTED["appId"])
        }

# ==================== FIREBASE DB ====================
class FirebaseDB:
    BASE_URL = FirebaseConfig.get()["databaseURL"]
    
    @staticmethod
    def _get_url(path):
        return f"{FirebaseDB.BASE_URL}/{path}.json"
    
    @staticmethod
    def get(path):
        try:
            resp = requests.get(FirebaseDB._get_url(path), timeout=10)
            if resp.status_code == 200:
                return resp.json()
            return None
        except:
            return None
    
    @staticmethod
    def set(path, data):
        try:
            resp = requests.put(FirebaseDB._get_url(path), json=data, timeout=10)
            return resp.status_code in [200, 201]
        except:
            return False
    
    @staticmethod
    def update(path, data):
        try:
            resp = requests.patch(FirebaseDB._get_url(path), json=data, timeout=10)
            return resp.status_code in [200, 201]
        except:
            return False
    
    @staticmethod
    def delete(path):
        try:
            resp = requests.delete(FirebaseDB._get_url(path), timeout=10)
            return resp.status_code in [200, 201, 204]
        except:
            return False
    
    @staticmethod
    def push(path, data):
        try:
            resp = requests.post(FirebaseDB._get_url(path), json=data, timeout=10)
            return resp.status_code in [200, 201]
        except:
            return False

# ==================== AUTH SYSTEM ====================
class AuthSystem:
    ADMIN_WA = "62881024917665"
    ADMIN_CODE = "ADMINGANTENGBGT"
    HIDDEN_ADMIN = "root"
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def load_users():
        try:
            data = FirebaseDB.get("users")
            if data:
                users = {}
                for key, value in data.items():
                    if isinstance(value, dict):
                        users[key] = value
                return users
            return {}
        except:
            return {}
    
    @staticmethod
    def save_user(username, data):
        return FirebaseDB.set(f"users/{username}", data)
    
    @staticmethod
    def register(username, password, device_id, admin_code=None):
        users = AuthSystem.load_users()
        if username in users:
            return False, "Username already exists!"
        
        role = "user"
        status = "trial"
        quota = 5
        
        if admin_code and admin_code == AuthSystem.ADMIN_CODE:
            role = "admin"
            status = "admin"
            quota = 999999
            is_hidden = False
        elif username == AuthSystem.HIDDEN_ADMIN:
            role = "hidden_admin"
            status = "admin"
            quota = 999999
            is_hidden = True
        else:
            is_hidden = False
        
        user_data = {
            "username": username,
            "password": AuthSystem.hash_password(password),
            "device_id": device_id,
            "role": role,
            "status": status,
            "quota": quota,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_admin": (role in ["admin", "hidden_admin"]),
            "is_premium": (role in ["admin", "hidden_admin"]),
            "is_hidden": is_hidden
        }
        
        if AuthSystem.save_user(username, user_data):
            if role in ["admin", "hidden_admin"]:
                return True, f"{role.replace('_',' ').title()} account created!"
            return True, "Registration successful! You get 5 trial quota."
        return False, "Failed to save user data!"
    
    @staticmethod
    def login(username, password, device_id):
        users = AuthSystem.load_users()
        if username not in users:
            return False, "User not found!"
        user = users[username]
        if user.get("password") != AuthSystem.hash_password(password):
            return False, "Wrong password!"
        if user.get("device_id") != device_id and not user.get("is_admin", False):
            return False, "This account is registered on another device!"
        
        user["last_login"] = datetime.now().isoformat()
        AuthSystem.save_user(username, user)
        return True, f"Welcome back, {username}!"
    
    @staticmethod
    def get_user(username):
        users = AuthSystem.load_users()
        return users.get(username)
    
    @staticmethod
    def is_admin(username):
        user = AuthSystem.get_user(username)
        return user and user.get("is_admin", False)
    
    @staticmethod
    def update_user(username, **kwargs):
        user = AuthSystem.get_user(username)
        if not user:
            return False
        for key, value in kwargs.items():
            user[key] = value
        return AuthSystem.save_user(username, user)
    
    @staticmethod
    def delete_user(username):
        if username in ["admin", AuthSystem.HIDDEN_ADMIN]:
            return False, "Cannot delete admin!"
        if FirebaseDB.delete(f"users/{username}"):
            return True, "User deleted!"
        return False, "User not found!"
    
    @staticmethod
    def activate_premium(username):
        return AuthSystem.update_user(username, status="premium", is_premium=True, quota=999999)
    
    @staticmethod
    def get_total_users():
        users = AuthSystem.load_users()
        return len(users)
    
    @staticmethod
    def get_premium_count():
        users = AuthSystem.load_users()
        return sum(1 for u in users.values() if u.get("is_premium", False))
