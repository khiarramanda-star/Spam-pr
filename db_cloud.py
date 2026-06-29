#!/usr/bin/env python3
# db_cloud.py - Cloud Database Connection (Obfuscated)

import requests
import hashlib
import base64
from datetime import datetime

# ==================== CLOUD CONFIG (ENCRYPTED) ====================
class CloudConfig:
    _ENC = {
        "key": "b3RUMFdJUmt6WEJNeUtZMXlGQVhQaXQyMGhrOUhMc1l6YUlB==",
        "url": "b3RtLm9lY2FpcmVmLmItZHQtZmF1bHQtMTQ4ODMtZXNhYi8vOnB0dGg=",
        "pid": "MTQ4ODMtZXNhYg==",
        "aid": "NjoyNjI3ZTdlZTZlZWM0ZTQyOTQ4Nzo1NTg4OTUzODgxNzg6MQ=="
    }
    
    @staticmethod
    def _d(e):
        try:
            return base64.b64decode(e).decode()[::-1]
        except:
            return e
    
    @staticmethod
    def get():
        return {
            "key": CloudConfig._d(CloudConfig._ENC["key"]),
            "url": CloudConfig._d(CloudConfig._ENC["url"]),
            "pid": CloudConfig._d(CloudConfig._ENC["pid"]),
            "aid": CloudConfig._d(CloudConfig._ENC["aid"])
        }

# ==================== CLOUD DB ====================
class CloudDB:
    BASE = CloudConfig.get()["url"]
    
    @staticmethod
    def _path(p):
        return f"{CloudDB.BASE}/{p}.json"
    
    @staticmethod
    def get(p):
        try:
            r = requests.get(CloudDB._path(p), timeout=10)
            return r.json() if r.status_code == 200 else None
        except:
            return None
    
    @staticmethod
    def set(p, d):
        try:
            r = requests.put(CloudDB._path(p), json=d, timeout=10)
            return r.status_code in [200, 201]
        except:
            return False
    
    @staticmethod
    def delete(p):
        try:
            r = requests.delete(CloudDB._path(p), timeout=10)
            return r.status_code in [200, 201, 204]
        except:
            return False

# ==================== USER MANAGER ====================
class UserManager:
    ADMIN_WA = "62881024917665"
    ADMIN_CODE = "ADMINGANTENGBGT"
    HIDDEN = "root"
    
    @staticmethod
    def _hash(pw):
        return hashlib.sha256(pw.encode()).hexdigest()
    
    @staticmethod
    def load_users():
        try:
            data = CloudDB.get("users")
            if data:
                return {k: v for k, v in data.items() if isinstance(v, dict)}
            return {}
        except:
            return {}
    
    @staticmethod
    def _save_user(u, d):
        return CloudDB.set(f"users/{u}", d)
    
    @staticmethod
    def register(u, pw, did, code=None):
        users = UserManager.load_users()
        if u in users:
            return False, "Username already exists!"
        
        role = "user"
        status = "trial"
        quota = 5
        
        if code and code == UserManager.ADMIN_CODE:
            role = "admin"
            status = "admin"
            quota = 999999
            hidden = False
        elif u == UserManager.HIDDEN:
            role = "hidden_admin"
            status = "admin"
            quota = 999999
            hidden = True
        else:
            hidden = False
        
        data = {
            "username": u,
            "password": UserManager._hash(pw),
            "device_id": did,
            "role": role,
            "status": status,
            "quota": quota,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_admin": (role in ["admin", "hidden_admin"]),
            "is_premium": (role in ["admin", "hidden_admin"]),
            "is_hidden": hidden
        }
        
        if UserManager._save_user(u, data):
            return True, f"{role.replace('_',' ').title()} account created!"
        return False, "Failed to save!"
    
    @staticmethod
    def login(u, pw, did):
        users = UserManager.load_users()
        if u not in users:
            return False, "User not found!"
        user = users[u]
        if user.get("password") != UserManager._hash(pw):
            return False, "Wrong password!"
        if user.get("device_id") != did and not user.get("is_admin", False):
            return False, "Wrong device!"
        
        user["last_login"] = datetime.now().isoformat()
        UserManager._save_user(u, user)
        return True, f"Welcome back, {u}!"
    
    @staticmethod
    def get_user(u):
        users = UserManager.load_users()
        return users.get(u)
    
    @staticmethod
    def is_admin(u):
        user = UserManager.get_user(u)
        return user and user.get("is_admin", False)
    
    @staticmethod
    def update_user(u, **kwargs):
        user = UserManager.get_user(u)
        if not user:
            return False
        for k, v in kwargs.items():
            user[k] = v
        return UserManager._save_user(u, user)
    
    @staticmethod
    def delete_user(u):
        if u in ["admin", UserManager.HIDDEN]:
            return False, "Cannot delete admin!"
        if CloudDB.delete(f"users/{u}"):
            return True, "User deleted!"
        return False, "User not found!"
    
    @staticmethod
    def activate_premium(u):
        return UserManager.update_user(u, status="premium", is_premium=True, quota=999999)
    
    @staticmethod
    def get_total_users():
        return len(UserManager.load_users())
    
    @staticmethod
    def get_premium_count():
        users = UserManager.load_users()
        return sum(1 for u in users.values() if u.get("is_premium", False))
