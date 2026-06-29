#!/usr/bin/env python3
# utils.py - Utility Functions

import random
import re

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

def random_ua():
    uas = [
        'Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/120.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 Chrome/119.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 12) AppleWebKit/537.36 Chrome/118.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 Version/17.0 Mobile/15E148 Safari/604.1',
    ]
    return random.choice(uas)

def get_random_name():
    names = ['User', 'Test', 'Demo', 'Coba', 'Uji', 'Sample', 'Bisnis', 'Agen']
    return random.choice(names) + ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=random.randint(3,6)))

def get_random_email():
    return get_random_name().lower() + str(random.randint(100,999)) + '@gmail.com'

def get_random_password():
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%'
    return 'Pass' + ''.join(random.choices(chars, k=6)) + '!'
