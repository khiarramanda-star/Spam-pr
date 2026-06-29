#!/usr/bin/env python3
# proxy_manager.py - 500+ Proxy dengan Auto-Refresh

import requests
import random
import time
import re
from urllib.parse import urlparse

# ==================== PROXY SOURCES ====================
PROXY_SOURCES = [
    # Primary sources
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/opsxcq/proxy-list/master/list.txt",
    "https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies.txt",
    
    # Backup sources
    "https://proxylist.geonode.com/api/proxy-list?limit=500&page=1&sort_by=lastChecked&sort_type=desc",
    "https://www.proxy-list.download/api/v1/get?type=http",
    "https://www.proxy-list.download/api/v1/get?type=https",
    "https://www.proxy-list.download/api/v1/get?type=socks4",
    "https://www.proxy-list.download/api/v1/get?type=socks5",
]

# ==================== DEFAULT PROXIES (FALLBACK) ====================
DEFAULT_PROXIES = [
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
    # Singapore
    "http://139.162.78.109:8080",
    "http://139.162.78.110:8080",
    "http://139.162.78.111:8080",
    "http://139.162.78.112:8080",
    "http://139.162.78.113:8080",
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
    # Europe
    "http://51.75.126.134:3128",
    "http://51.75.126.135:3128",
    "http://51.75.126.136:3128",
    "http://51.75.126.137:3128",
    "http://51.75.126.138:3128",
    # Asia
    "http://43.153.4.79:8888",
    "http://43.153.4.80:8888",
    "http://43.153.4.81:8888",
    "http://43.153.4.82:8888",
    "http://43.153.4.83:8888",
    "http://43.153.4.84:8888",
    "http://43.153.4.85:8888",
    "http://43.153.4.86:8888",
]

# ==================== PROXY MANAGER ====================
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.failed_proxies = set()
        self.used_proxies = set()
        self.last_refresh = 0
        self.refresh_interval = 300  # 5 menit
        self.current_index = 0
        self.lock = False
    
    def load_proxies(self, force=False):
        """Load proxies from all sources"""
        if self.lock:
            return self.proxies
        
        self.lock = True
        try:
            # Refresh every 5 minutes
            if not force and time.time() - self.last_refresh < self.refresh_interval:
                self.lock = False
                return self.proxies
            
            all_proxies = []
            
            # Try all sources
            for url in PROXY_SOURCES:
                try:
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        for line in resp.text.splitlines():
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Clean proxy format
                                if '://' in line:
                                    proxy = line
                                else:
                                    # Check if it's IP:PORT format
                                    if re.match(r'^\d+\.\d+\.\d+\.\d+:\d+$', line):
                                        proxy = f"http://{line}"
                                    elif re.match(r'^\[.*\]:\d+$', line):
                                        proxy = f"http://{line}"
                                    else:
                                        proxy = f"http://{line}"
                                
                                if self._validate_proxy(proxy):
                                    all_proxies.append(proxy)
                    time.sleep(0.5)  # Jangan banjir request
                except:
                    continue
            
            # Remove duplicates
            all_proxies = list(dict.fromkeys(all_proxies))
            
            # Remove failed proxies
            self.proxies = [p for p in all_proxies if p not in self.failed_proxies]
            
            # If no proxies, use defaults
            if not self.proxies:
                self.proxies = DEFAULT_PROXIES.copy()
            
            # Remove used proxies if we have enough
            if len(self.proxies) > 50:
                self.proxies = [p for p in self.proxies if p not in self.used_proxies]
            
            # If still empty, use defaults
            if not self.proxies:
                self.proxies = DEFAULT_PROXIES.copy()
                self.used_proxies.clear()
                self.failed_proxies.clear()
            
            self.last_refresh = time.time()
            
        except:
            if not self.proxies:
                self.proxies = DEFAULT_PROXIES.copy()
        
        self.lock = False
        return self.proxies
    
    def _validate_proxy(self, proxy):
        """Validate proxy format"""
        try:
            parsed = urlparse(proxy)
            if parsed.scheme in ['http', 'https', 'socks4', 'socks5'] and parsed.netloc:
                return True
            return False
        except:
            return False
    
    def get_proxy(self):
        """Get next available proxy"""
        if not self.proxies:
            self.load_proxies()
        
        if not self.proxies:
            return None
        
        # Try to find a fresh proxy
        for _ in range(min(10, len(self.proxies))):
            proxy = self.proxies[self.current_index % len(self.proxies)]
            self.current_index += 1
            if proxy not in self.failed_proxies and proxy not in self.used_proxies:
                self.used_proxies.add(proxy)
                return proxy
        
        # If all proxies are used, reset
        self.used_proxies.clear()
        if self.proxies:
            proxy = self.proxies[self.current_index % len(self.proxies)]
            self.current_index += 1
            return proxy
        
        return None
    
    def mark_failed(self, proxy):
        """Mark proxy as failed"""
        if proxy:
            self.failed_proxies.add(proxy)
            if proxy in self.proxies:
                self.proxies.remove(proxy)
    
    def mark_success(self, proxy):
        """Mark proxy as success"""
        if proxy and proxy in self.failed_proxies:
            self.failed_proxies.remove(proxy)
    
    def get_proxy_dict(self, proxy_url):
        """Convert proxy string to dict for requests"""
        if not proxy_url:
            return None
        
        parsed = urlparse(proxy_url)
        scheme = parsed.scheme or 'http'
        return {
            'http': f"{scheme}://{parsed.netloc}",
            'https': f"{scheme}://{parsed.netloc}"
        }
    
    def get_stats(self):
        """Get proxy statistics"""
        return {
            'total': len(self.proxies),
            'failed': len(self.failed_proxies),
            'used': len(self.used_proxies),
            'last_refresh': self.last_refresh
        }

# ==================== SINGLETON ====================
_proxy_manager = None

def get_proxy_manager():
    global _proxy_manager
    if _proxy_manager is None:
        _proxy_manager = ProxyManager()
    return _proxy_manager

def safe_request(method, url, **kwargs):
    """Send request with proxy rotation"""
    pm = get_proxy_manager()
    timeout = kwargs.pop('timeout', 15)
    headers = kwargs.pop('headers', {})
    data = kwargs.pop('data', None)
    json_data = kwargs.pop('json', None)
    cookies = kwargs.pop('cookies', None)
    
    for attempt in range(3):
        proxy = pm.get_proxy()
        proxy_dict = pm.get_proxy_dict(proxy)
        
        try:
            req_kwargs = {
                'headers': headers,
                'timeout': timeout,
                'verify': False,
                'allow_redirects': True,
            }
            if cookies: req_kwargs['cookies'] = cookies
            if proxy_dict: req_kwargs['proxies'] = proxy_dict
            if data is not None: req_kwargs['data'] = data
            elif json_data is not None: req_kwargs['json'] = json_data
            
            if method.upper() == 'GET':
                resp = requests.get(url, **req_kwargs)
            elif method.upper() == 'POST':
                resp = requests.post(url, **req_kwargs)
            elif method.upper() == 'PUT':
                resp = requests.put(url, **req_kwargs)
            elif method.upper() == 'DELETE':
                resp = requests.delete(url, **req_kwargs)
            else:
                resp = requests.request(method, url, **req_kwargs)
            
            if resp.status_code < 500:
                pm.mark_success(proxy)
                return resp
            else:
                pm.mark_failed(proxy)
        except:
            pm.mark_failed(proxy)
            continue
    
    # Fallback tanpa proxy
    try:
        req_kwargs = {
            'headers': headers,
            'timeout': timeout,
            'verify': False,
        }
        if cookies: req_kwargs['cookies'] = cookies
        if data is not None: req_kwargs['data'] = data
        elif json_data is not None: req_kwargs['json'] = json_data
        
        if method.upper() == 'GET':
            return requests.get(url, **req_kwargs)
        else:
            return requests.post(url, **req_kwargs)
    except:
        return None

# ==================== TEST ====================
if __name__ == "__main__":
    pm = get_proxy_manager()
    pm.load_proxies(force=True)
    stats = pm.get_stats()
    print(f"Total proxies: {stats['total']}")
    print(f"Failed: {stats['failed']}")
    print(f"Used: {stats['used']}")
    print("\nSample proxies:")
    for p in pm.proxies[:10]:
        print(f"  {p}")
