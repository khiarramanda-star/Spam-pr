#!/usr/bin/env python3
# main.py - OTP BOMBER ULTIMATE v10.0 - FIREBASE REAL
# "I just give the tools, whether they're used right or not is your business, boss."

import sys
import time
import platform
import hashlib
import json
import os
import uuid
import requests
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

# ==================== FIREBASE CONFIG ====================
# 🔥 REAL FIREBASE CONFIG FROM BOSS
FIREBASE_CONFIG = {
    "apiKey": "AIzaSyDLHk9h02tiPAFXy1YKIbMXuHZkRIwGtTo",
    "databaseURL": "https://base-38841-default-rtdb.firebaseio.com",
    "projectId": "base-38841",
    "appId": "1:878559883155:android:784ba9264e18eece7e8266"
}

# ==================== FIREBASE HELPER ====================
class FirebaseDB:
    BASE_URL = FIREBASE_CONFIG["databaseURL"]
    
    @staticmethod
    def _get_url(path):
        return f"{FirebaseDB.BASE_URL}/{path}.json"
    
    @staticmethod
    def get(path):
        try:
            url = FirebaseDB._get_url(path)
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                return resp.json()
            return None
        except Exception as e:
            print(f"{Fore.RED}[!] Firebase get error: {e}{Style.RESET_ALL}")
            return None
    
    @staticmethod
    def set(path, data):
        try:
            url = FirebaseDB._get_url(path)
            resp = requests.put(url, json=data, timeout=15)
            return resp.status_code in [200, 201]
        except Exception as e:
            print(f"{Fore.RED}[!] Firebase set error: {e}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def push(path, data):
        try:
            url = FirebaseDB._get_url(path)
            resp = requests.post(url, json=data, timeout=15)
            return resp.status_code in [200, 201]
        except Exception as e:
            print(f"{Fore.RED}[!] Firebase push error: {e}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def update(path, data):
        try:
            url = FirebaseDB._get_url(path)
            resp = requests.patch(url, json=data, timeout=15)
            return resp.status_code in [200, 201]
        except Exception as e:
            print(f"{Fore.RED}[!] Firebase update error: {e}{Style.RESET_ALL}")
            return False
    
    @staticmethod
    def delete(path):
        try:
            url = FirebaseDB._get_url(path)
            resp = requests.delete(url, timeout=15)
            return resp.status_code in [200, 201, 204]
        except Exception as e:
            print(f"{Fore.RED}[!] Firebase delete error: {e}{Style.RESET_ALL}")
            return False

# ==================== USER AUTH SYSTEM ====================
class AuthSystem:
    ADMIN_WA = "62881024917665"
    ADMIN_CODE = "ADMINGANTENGBGT"
    
    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def load_users():
        try:
            data = FirebaseDB.get("users")
            if data:
                # Convert object to dict
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
        try:
            return FirebaseDB.set(f"users/{username}", data)
        except:
            return False
    
    @staticmethod
    def register(username, password, device_id, admin_code=None):
        users = AuthSystem.load_users()
        if username in users:
            return False, "Username already exists!"
        
        # Check if this is admin registration
        role = "user"
        status = "trial"
        quota = 5
        
        if admin_code and admin_code == AuthSystem.ADMIN_CODE:
            role = "admin"
            status = "admin"
            quota = 999999
        
        user_data = {
            "username": username,
            "password": AuthSystem.hash_password(password),
            "device_id": device_id,
            "role": role,
            "status": status,
            "quota": quota,
            "created_at": datetime.now().isoformat(),
            "last_login": None,
            "is_admin": (role == "admin"),
            "is_premium": False
        }
        
        if AuthSystem.save_user(username, user_data):
            if role == "admin":
                return True, "Admin account created successfully!"
            return True, "Registration successful! You get 5 trial quota."
        else:
            return False, "Failed to save user data to Firebase!"
    
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
        
        # Update last login
        user["last_login"] = datetime.now().isoformat()
        AuthSystem.save_user(username, user)
        
        # Save session
        with open(".session", 'w') as f:
            json.dump({"username": username, "device_id": device_id}, f)
        return True, f"Welcome back, {username}!"
    
    @staticmethod
    def get_session():
        try:
            with open(".session", 'r') as f:
                return json.load(f)
        except:
            return None
    
    @staticmethod
    def logout():
        try:
            os.remove(".session")
            return True
        except:
            return False
    
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
        if username == "admin":
            return False, "Cannot delete admin!"
        users = AuthSystem.load_users()
        if username in users:
            if FirebaseDB.delete(f"users/{username}"):
                return True, "User deleted!"
        return False, "User not found!"
    
    @staticmethod
    def get_all_users():
        users = AuthSystem.load_users()
        return {k: v for k, v in users.items() if k != "admin"}
    
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
    
    @staticmethod
    def get_trial_count():
        users = AuthSystem.load_users()
        return sum(1 for u in users.values() if not u.get("is_premium", False) and u.get("role") != "admin")

# ==================== UI & COLORS ====================
class Colors:
    HEADER = Fore.MAGENTA + Style.BRIGHT
    BLUE = Fore.CYAN + Style.BRIGHT
    GREEN = Fore.GREEN + Style.BRIGHT
    YELLOW = Fore.YELLOW + Style.BRIGHT
    RED = Fore.RED + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Style.RESET_ALL
    DIM = Fore.WHITE + Style.DIM
    CYAN = Fore.CYAN
    GOLD = Fore.YELLOW + Style.BRIGHT

C = Colors()

def clear_screen():
    os.system('clear' if os.name == 'posix' else 'cls')

def print_banner():
    banner = f"""
{C.HEADER}╔═══════════════════════════════════════════════════════════════════╗
║                                                                   ║
║   {C.GREEN}██████╗ ████████╗██████╗     ██████╗  ██████╗ ███╗   ███╗{C.HEADER}   ║
║   {C.GREEN}██╔══██╗╚══██╔══╝██╔══██╗    ██╔══██╗██╔═══██╗████╗ ████║{C.HEADER}   ║
║   {C.GREEN}██████╔╝   ██║   ██████╔╝    ██████╔╝██║   ██║██╔████╔██║{C.HEADER}   ║
║   {C.GREEN}██╔═══╝    ██║   ██╔══██╗    ██╔══██╗██║   ██║██║╚██╔╝██║{C.HEADER}   ║
║   {C.GREEN}██║        ██║   ██║  ██║    ██████╔╝╚██████╔╝██║ ╚═╝ ██║{C.HEADER}   ║
║   {C.GREEN}╚═╝        ╚═╝   ╚═╝  ╚═╝    ╚═════╝  ╚═════╝ ╚═╝     ╚═╝{C.HEADER}   ║
║                                                                   ║
║            {C.YELLOW}🔥 OTP BOMBER V1 {C.HEADER}            ║
║            {C.WHITE}🔥 FULL ADMIN PANEL  {C.HEADER}             ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
{C.RESET}
    """
    print(banner)

def print_admin_badge():
    print(f"{C.RED}╔═══════════════════════════════════════════════════════════════════╗")
    print(f"{C.RED}║                     👑 ADMIN MODE ACTIVE                        ║")
    print(f"{C.RED}╚═══════════════════════════════════════════════════════════════════╝{C.RESET}")

def get_input(prompt, color=C.CYAN):
    return input(f"{color}[?] {prompt}: {C.WHITE}")

def get_password_input(prompt):
    import getpass
    return getpass.getpass(f"{C.CYAN}[?] {prompt}: {C.WHITE}")

def print_boxed(text, color=C.CYAN, width=60):
    lines = text.split('\n')
    max_len = max(len(line) for line in lines)
    if max_len > width - 4:
        width = max_len + 4
    print(f"{color}┌{'─' * (width - 2)}┐")
    for line in lines:
        padding = width - len(line) - 4
        print(f"{color}│ {line}{' ' * padding} │")
    print(f"{color}└{'─' * (width - 2)}┘{C.RESET}")

def loading_animation(text, duration=2):
    chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    i = 0
    while time.time() < end_time:
        sys.stdout.write(f'\r{C.YELLOW}{chars[i % len(chars)]} {text}{C.RESET}')
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    sys.stdout.write('\r' + ' ' * 50 + '\r')

# ==================== AUTH MENU ====================
def auth_menu():
    clear_screen()
    print_banner()
    print()
    print(f"  {C.GREEN}[1]{C.RESET} Login")
    print(f"  {C.GREEN}[2]{C.RESET} Register")
    print(f"  {C.GREEN}[3]{C.RESET} Register as Admin {C.RED}(with code){C.RESET}")
    print(f"  {C.GREEN}[4]{C.RESET} Exit")
    print()
    choice = get_input("Pilih menu (1/2/3/4)", C.CYAN)
    
    if choice == "1":
        return login_menu()
    elif choice == "2":
        return register_menu()
    elif choice == "3":
        return admin_register_menu()
    elif choice == "4":
        print(f"\n{C.GREEN}Goodbye!{C.RESET}")
        sys.exit(0)
    else:
        print(f"{C.RED}Invalid choice!{C.RESET}")
        time.sleep(1)
        return auth_menu()

def login_menu():
    clear_screen()
    print_banner()
    print_boxed("🔐 LOGIN", C.CYAN)
    print()
    username = get_input("Username", C.CYAN)
    password = get_password_input("Password")
    device_id = platform.node()
    
    loading_animation("Connecting to Firebase...", 1.5)
    
    success, message = AuthSystem.login(username, password, device_id)
    if success:
        print(f"\n{C.GREEN}✅ {message}{C.RESET}")
        time.sleep(1.5)
        return username
    else:
        print(f"\n{C.RED}❌ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return auth_menu()

def register_menu():
    clear_screen()
    print_banner()
    print_boxed("📝 REGISTER", C.GREEN)
    print()
    username = get_input("Username (min 3 chars)", C.CYAN)
    if len(username) < 3:
        print(f"{C.RED}Username minimal 3 karakter!{C.RESET}")
        time.sleep(1)
        return register_menu()
    
    password = get_password_input("Password (min 4 chars)")
    if len(password) < 4:
        print(f"{C.RED}Password minimal 4 karakter!{C.RESET}")
        time.sleep(1)
        return register_menu()
    
    confirm = get_password_input("Confirm Password")
    if password != confirm:
        print(f"{C.RED}Password tidak cocok!{C.RESET}")
        time.sleep(1)
        return register_menu()
    
    device_id = platform.node()
    
    loading_animation("Registering to Firebase...", 1.5)
    
    success, message = AuthSystem.register(username, password, device_id)
    
    if success:
        print(f"\n{C.GREEN}✅ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk login...{C.RESET}")
        return login_menu()
    else:
        print(f"\n{C.RED}❌ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return auth_menu()

def admin_register_menu():
    clear_screen()
    print_banner()
    print_boxed("👑 REGISTER AS ADMIN", C.RED)
    print()
    admin_code = get_input("Admin Code", C.RED)
    if admin_code != AuthSystem.ADMIN_CODE:
        print(f"{C.RED}❌ Invalid admin code!{C.RESET}")
        time.sleep(2)
        return auth_menu()
    
    username = get_input("Admin Username", C.CYAN)
    if len(username) < 3:
        print(f"{C.RED}Username minimal 3 karakter!{C.RESET}")
        time.sleep(1)
        return admin_register_menu()
    
    password = get_password_input("Admin Password")
    if len(password) < 4:
        print(f"{C.RED}Password minimal 4 karakter!{C.RESET}")
        time.sleep(1)
        return admin_register_menu()
    
    confirm = get_password_input("Confirm Password")
    if password != confirm:
        print(f"{C.RED}Password tidak cocok!{C.RESET}")
        time.sleep(1)
        return admin_register_menu()
    
    device_id = platform.node()
    
    loading_animation("Creating admin account...", 1.5)
    
    success, message = AuthSystem.register(username, password, device_id, admin_code)
    
    if success:
        print(f"\n{C.GREEN}✅ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk login...{C.RESET}")
        return login_menu()
    else:
        print(f"\n{C.RED}❌ {message}{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return auth_menu()

# ==================== ADMIN PANEL ====================
def admin_panel(username):
    while True:
        clear_screen()
        print_banner()
        print_admin_badge()
        print()
        print(f"{C.CYAN}┌─────────────────────────────────────────────────────────────┐")
        print(f"{C.CYAN}│{C.WHITE}  👑 ADMIN PANEL - {username}{' ' * (35 - len(username))}{C.CYAN}│")
        print(f"{C.CYAN}└─────────────────────────────────────────────────────────────┘{C.RESET}")
        print()
        
        total_users = AuthSystem.get_total_users()
        premium_count = AuthSystem.get_premium_count()
        trial_count = AuthSystem.get_trial_count()
        
        print(f"{C.CYAN}📊 STATISTICS:{C.RESET}")
        print(f"  {C.WHITE}Total Users    : {C.GREEN}{total_users}")
        print(f"  {C.WHITE}Premium Users  : {C.GOLD}{premium_count}")
        print(f"  {C.WHITE}Trial Users    : {C.YELLOW}{trial_count}")
        print()
        
        print(f"{C.CYAN}🛠 MENU ADMIN:{C.RESET}")
        print(f"  {C.GREEN}[1]{C.RESET} 📋 List All Users")
        print(f"  {C.GREEN}[2]{C.RESET} 👑 Activate Premium User")
        print(f"  {C.GREEN}[3]{C.RESET} 🗑️  Delete User")
        print(f"  {C.GREEN}[4]{C.RESET} 🔄 Refresh Data")
        print(f"  {C.GREEN}[5]{C.RESET} 📱 Contact Admin WA")
        print(f"  {C.GREEN}[6]{C.RESET} 🚪 Logout")
        print()
        choice = get_input("Pilih menu (1-6)", C.CYAN)
        
        if choice == "1":
            list_users()
        elif choice == "2":
            activate_premium()
        elif choice == "3":
            delete_user()
        elif choice == "4":
            print(f"{C.GREEN}✅ Data refreshed from Firebase!{C.RESET}")
            time.sleep(1)
        elif choice == "5":
            show_admin_wa()
        elif choice == "6":
            AuthSystem.logout()
            print(f"{C.GREEN}Logout berhasil!{C.RESET}")
            time.sleep(1)
            return auth_menu()
        else:
            print(f"{C.RED}Pilihan tidak valid!{C.RESET}")
            time.sleep(1)

def list_users():
    clear_screen()
    print_banner()
    print_boxed("📋 LIST ALL USERS", C.CYAN)
    print()
    
    loading_animation("Loading data from Firebase...", 1)
    
    users = AuthSystem.load_users()
    
    if not users:
        print(f"{C.YELLOW}Belum ada user terdaftar.{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return
    
    print(f"{C.WHITE}{'Username':<20} {'Status':<12} {'Quota':<8} {'Premium'}{C.RESET}")
    print(f"{C.DIM}{'-' * 55}{C.RESET}")
    
    for username, data in users.items():
        status = data.get('status', 'trial')
        quota = data.get('quota', 0)
        is_premium = data.get('is_premium', False)
        premium_status = f"{C.GREEN}✅{C.RESET}" if is_premium else f"{C.RED}❌{C.RESET}"
        status_color = C.GREEN if status == 'premium' else C.YELLOW if status == 'admin' else C.DIM
        print(f"{username:<20} {status_color}{status:<12}{C.RESET} {quota:<8} {premium_status}")
    
    print()
    total = len(users)
    print(f"{C.CYAN}Total: {C.WHITE}{total} users{C.RESET}")
    input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")

def activate_premium():
    clear_screen()
    print_banner()
    print_boxed("👑 ACTIVATE PREMIUM", C.GOLD)
    print()
    username = get_input("Username yang akan di-activate premium", C.CYAN)
    
    user = AuthSystem.get_user(username)
    if not user:
        print(f"{C.RED}❌ User not found!{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return
    
    if user.get('is_premium', False):
        print(f"{C.YELLOW}⚠️ User {username} sudah premium!{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return
    
    confirm = get_input(f"Activate premium for {username}? (y/n)", C.YELLOW)
    if confirm.lower() != 'y':
        print(f"{C.YELLOW}❌ Cancelled!{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return
    
    loading_animation("Activating premium...", 1.5)
    
    if AuthSystem.activate_premium(username):
        print(f"{C.GREEN}✅ {username} now is PREMIUM USER!{C.RESET}")
        # Send notification to admin WA (optional)
        print(f"{C.DIM}📱 Admin WA: {AuthSystem.ADMIN_WA}{C.RESET}")
    else:
        print(f"{C.RED}❌ Failed to activate premium!{C.RESET}")
    
    input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")

def delete_user():
    clear_screen()
    print_banner()
    print_boxed("🗑️ DELETE USER", C.RED)
    print()
    username = get_input("Username yang akan dihapus", C.CYAN)
    
    if username == "admin":
        print(f"{C.RED}❌ Cannot delete admin user!{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return
    
    user = AuthSystem.get_user(username)
    if not user:
        print(f"{C.RED}❌ User not found!{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return
    
    confirm = get_input(f"Delete user {username}? (y/n)", C.RED)
    if confirm.lower() != 'y':
        print(f"{C.YELLOW}❌ Cancelled!{C.RESET}")
        input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
        return
    
    loading_animation("Deleting user from Firebase...", 1.5)
    
    success, message = AuthSystem.delete_user(username)
    if success:
        print(f"{C.GREEN}✅ {message}{C.RESET}")
    else:
        print(f"{C.RED}❌ {message}{C.RESET}")
    
    input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")

def show_admin_wa():
    clear_screen()
    print_banner()
    print_boxed("📱 CONTACT ADMIN", C.GREEN)
    print()
    print(f"{C.WHITE}Admin WhatsApp: {C.GREEN}{AuthSystem.ADMIN_WA}{C.RESET}")
    print()
    print(f"{C.YELLOW}Untuk pembelian premium, hubungi admin via WhatsApp.{C.RESET}")
    print(f"{C.DIM}Kirim Device ID Anda untuk aktivasi premium.{C.RESET}")
    print()
    print(f"{C.CYAN}Device ID: {C.WHITE}{platform.node()}{C.RESET}")
    print()
    print(f"{C.DIM}Link WhatsApp:{C.RESET}")
    print(f"  {C.BLUE}https://wa.me/{AuthSystem.ADMIN_WA}{C.RESET}")
    print()
    input(f"{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")

def show_buy_guide():
    clear_screen()
    print_banner()
    print_boxed("🛒 BELI LISENSI PREMIUM", C.GOLD)
    print()
    print(f"{C.WHITE}Keuntungan Premium:{C.RESET}")
    print(f"  {C.GREEN}•{C.RESET} Akses FULL semua API (30+ API)")
    print(f"  {C.GREEN}•{C.RESET} Unlimited penggunaan (tanpa batas)")
    print(f"  {C.GREEN}•{C.RESET} Update tools & API baru")
    print(f"  {C.GREEN}•{C.RESET} Dukungan prioritas")
    print()
    print(f"{C.CYAN}Harga: {C.GREEN}Rp. 25.000 (sekali bayar){C.RESET}")
    print()
    print(f"{C.YELLOW}Cara Pembelian:{C.RESET}")
    print(f"  1. Chat admin via WhatsApp:")
    print(f"     {C.GREEN}📱 {AuthSystem.ADMIN_WA}{C.RESET}")
    print(f"     {C.BLUE}🔗 https://wa.me/{AuthSystem.ADMIN_WA}{C.RESET}")
    print(f"  2. Kirim Device ID: {C.WHITE}{platform.node()}{C.RESET}")
    print(f"  3. Lakukan pembayaran (QRIS/Transfer)")
    print(f"  4. Tunggu aktivasi (1-5 menit)")
    print()
    input(f"{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")

def show_about():
    clear_screen()
    print_banner()
    print_boxed("ℹ️ ABOUT TOOLS", C.BLUE)
    print()
    print(f"{C.WHITE}Nama    : OTP Bomber Ultimate")
    print(f"Versi   : 10.0")
    print(f"Author  : Kyriel")
    print(f"API     : 30+ Working WhatsApp OTP")
    print(f"DB      : Firebase Realtime Database")
    print(f"Admin   : {AuthSystem.ADMIN_WA}")
    print(f"Status  : {C.GREEN}Active{C.RESET}")
    print()
    print(f"{C.DIM}I just give the tools, whether they're used right or not is your business, boss.{C.RESET}")
    print()
    input(f"{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")

# ==================== MAIN MENU ====================
def main_menu(username):
    user_data = AuthSystem.get_user(username)
    if not user_data:
        AuthSystem.logout()
        return auth_menu()
    
    # Check if admin
    if user_data.get('is_admin', False):
        return admin_panel(username)
    
    status = user_data.get('status', 'trial')
    quota = user_data.get('quota', 5)
    is_premium = user_data.get('is_premium', False)
    
    while True:
        clear_screen()
        print_banner()
        print(f"{C.CYAN}┌─────────────────────────────────────────────────────────────┐")
        print(f"{C.CYAN}│{C.WHITE}  👤 {username}{' ' * (30 - len(username))}{C.CYAN}│")
        print(f"{C.CYAN}│{C.DIM}  Status: {C.YELLOW}{status.upper()}{C.DIM}  |  {C.GREEN}Quota: {quota}{' ' * (26 - len(str(quota)))}{C.CYAN}│")
        print(f"{C.CYAN}└─────────────────────────────────────────────────────────────┘{C.RESET}")
        print()
        
        total_users = AuthSystem.get_total_users()
        premium_count = AuthSystem.get_premium_count()
        print(f"{C.CYAN}├─ 📊 Total Users   : {C.WHITE}{total_users}")
        print(f"{C.CYAN}├─ 👑 Premium       : {C.GREEN}{premium_count}")
        print(f"{C.CYAN}└─ 🆓 Trial         : {C.YELLOW}{total_users - premium_count}{C.RESET}")
        print()
        
        if is_premium:
            print(f"{C.GOLD}⭐ PREMIUM ACTIVE - Full Access{C.RESET}")
            print()
            print(f"  {C.GREEN}[1]{C.RESET} 🔥 Single Round")
            print(f"  {C.GREEN}[2]{C.RESET} 🔁 Infinite Loop")
            print(f"  {C.GREEN}[3]{C.RESET} 📊 Check APIs")
            print(f"  {C.GREEN}[4]{C.RESET} ℹ️ About")
            print(f"  {C.GREEN}[5]{C.RESET} 🚪 Logout")
            print()
            choice = get_input("Pilih menu (1-5)", C.CYAN)
            
            if choice == "1":
                try:
                    from main_engine import run_single_round
                    threads = get_thread_count()
                    run_single_round(threads=threads)
                except ImportError:
                    print(f"{C.RED}❌ main_engine.py not found!{C.RESET}")
                input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
            elif choice == "2":
                try:
                    from main_engine import run_infinite_loop
                    run_infinite_loop()
                except ImportError:
                    print(f"{C.RED}❌ main_engine.py not found!{C.RESET}")
                input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
            elif choice == "3":
                try:
                    from main_engine import show_apis
                    show_apis()
                except ImportError:
                    print(f"{C.RED}❌ main_engine.py not found!{C.RESET}")
                input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
            elif choice == "4":
                show_about()
            elif choice == "5":
                AuthSystem.logout()
                print(f"{C.GREEN}Logout berhasil!{C.RESET}")
                time.sleep(1)
                return auth_menu()
            else:
                print(f"{C.RED}Pilihan tidak valid!{C.RESET}")
                time.sleep(1)
        
        else:  # TRIAL
            print(f"{C.YELLOW}🆓 TRIAL MODE - Sisa Kuota: {quota}{C.RESET}")
            print(f"{C.DIM}Hanya bisa Single Round{C.RESET}")
            print()
            print(f"  {C.GREEN}[1]{C.RESET} 🔥 Single Round")
            print(f"  {C.GREEN}[2]{C.RESET} 🛒 Beli Premium")
            print(f"  {C.GREEN}[3]{C.RESET} ℹ️ About")
            print(f"  {C.GREEN}[4]{C.RESET} 🚪 Logout")
            print()
            choice = get_input("Pilih menu (1-4)", C.CYAN)
            
            if choice == "1":
                if quota <= 0:
                    print(f"{C.RED}❌ Kuota trial habis! Silakan beli premium.{C.RESET}")
                    time.sleep(2)
                    continue
                try:
                    from main_engine import run_single_round
                    run_single_round(threads=1)
                except ImportError:
                    print(f"{C.RED}❌ main_engine.py not found!{C.RESET}")
                # Reduce quota
                user_data = AuthSystem.get_user(username)
                if user_data:
                    new_quota = max(0, user_data.get('quota', 0) - 1)
                    AuthSystem.update_user(username, quota=new_quota)
                    quota = new_quota
                    print(f"{C.CYAN}📊 Sisa kuota: {quota}{C.RESET}")
                input(f"\n{C.YELLOW}Tekan Enter untuk kembali...{C.RESET}")
            elif choice == "2":
                show_buy_guide()
                user_data = AuthSystem.get_user(username)
                if user_data:
                    status = user_data.get('status', 'trial')
                    quota = user_data.get('quota', 5)
                    is_premium = user_data.get('is_premium', False)
            elif choice == "3":
                show_about()
            elif choice == "4":
                AuthSystem.logout()
                print(f"{C.GREEN}Logout berhasil!{C.RESET}")
                time.sleep(1)
                return auth_menu()
            else:
                print(f"{C.RED}Pilihan tidak valid!{C.RESET}")
                time.sleep(1)

def get_thread_count():
    clear_screen()
    print_banner()
    print_boxed("⚙️ PILIH THREAD", C.BLUE)
    print()
    print(f"  {C.GREEN}[1]{C.RESET} 1 Thread  {C.DIM}(slow){C.RESET}")
    print(f"  {C.GREEN}[2]{C.RESET} 2 Thread")
    print(f"  {C.GREEN}[3]{C.RESET} 3 Thread")
    print(f"  {C.GREEN}[4]{C.RESET} 4 Thread")
    print(f"  {C.GREEN}[5]{C.RESET} 5 Thread  {C.DIM}(recommended){C.RESET}")
    print(f"  {C.GREEN}[6]{C.RESET} 6 Thread")
    print(f"  {C.GREEN}[7]{C.RESET} 7 Thread")
    print(f"  {C.GREEN}[8]{C.RESET} 8 Thread")
    print(f"  {C.GREEN}[9]{C.RESET} 9 Thread")
    print(f"  {C.GREEN}[10]{C.RESET}10 Thread {C.DIM}(fast){C.RESET}")
    print()
    choice = get_input("Pilih thread (1-10, enter=1)", C.CYAN)
    try:
        threads = int(choice) if choice.strip() else 1
        return max(1, min(10, threads))
    except:
        return 1

# ==================== MAIN ====================
def main():
    print(f"{C.CYAN}🔥 Connecting to Firebase...{C.RESET}")
    loading_animation("Initializing Firebase connection...", 2)
    
    # Test Firebase connection
    try:
        test = FirebaseDB.get("users")
        if test is not None:
            print(f"{C.GREEN}✅ Firebase connected successfully!{C.RESET}")
        else:
            print(f"{C.YELLOW}⚠️ Firebase connected but no data yet.{C.RESET}")
    except:
        print(f"{C.YELLOW}⚠️ Firebase connection warning. Continuing...{C.RESET}")
    
    time.sleep(1)
    
    # Check for existing session
    session = AuthSystem.get_session()
    if session:
        username = session.get('username')
        user = AuthSystem.get_user(username)
        if user and user.get('device_id') == session.get('device_id'):
            main_menu(username)
            return
    
    # Start auth
    auth_menu()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{C.YELLOW}Exit by user...{C.RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{C.RED}Error: {e}{C.RESET}")
        sys.exit(1)
