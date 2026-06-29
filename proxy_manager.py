#!/usr/bin/env python3
# proxy_manager.py - Proxy Rotation & Management

import requests
import random
import time
import re
from urllib.parse import urlparse

# ==================== PROXY SOURCES ====================
PROXY_SOURCES = [
    "https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS.txt",
    "https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt",
]

# ==================== PROXY MANAGER ====================
class ProxyManager:
    def __init__(self):
        self.proxies = []
        self.current_index = 0
        self.failed_proxies = set()
        self.last_refresh = 0
        self.refresh_interval = 300  # 5 menit
        self.lock = False
    
    def load_proxies(self, force=False):
        """Load proxies from sources"""
        if self.lock:
            return self.proxies
        
        self.lock = True
        try:
            # Kalo masih fresh dan gak force, balik
            if not force and time.time() - self.last_refresh < self.refresh_interval:
                self.lock = False
                return self.proxies
            
            all_proxies = []
            
            for url in PROXY_SOURCES:
                try:
                    resp = requests.get(url, timeout=10)
                    if resp.status_code == 200:
                        for line in resp.text.splitlines():
                            line = line.strip()
                            if line and not line.startswith('#'):
                                # Format proxy
                                if '://' not in line:
                                    proxy = f"http://{line}"
                                else:
                                    proxy = line
                                if self._validate_proxy(proxy):
                                    all_proxies.append(proxy)
                except:
                    continue
            
            # Proxy default kalo gagal
            if not all_proxies:
                all_proxies = [
                    "http://103.175.42.147:80",
                    "http://103.175.42.157:80",
                    "http://103.175.42.155:80",
                    "http://103.146.145.142:8080",
                    "http://103.146.145.143:8080",
                    "http://103.158.188.12:8000",
                    "http://103.158.188.13:8000",
                    "http://103.158.188.14:8000",
                ]
            
            # Filter failed proxies
            self.proxies = [p for p in all_proxies if p not in self.failed_proxies]
            
            # Kalo semua proxy failed, reset failed list
            if not self.proxies:
                self.failed_proxies.clear()
                self.proxies = all_proxies
            
            self.last_refresh = time.time()
            
        except:
            pass
        
        self.lock = False
        return self.proxies
    
    def _validate_proxy(self, proxy):
        """Validasi format proxy"""
        try:
            parsed = urlparse(proxy)
            if parsed.scheme in ['http', 'https', 'socks5'] and parsed.netloc:
                return True
            return False
        except:
            return False
    
    def get_proxy(self):
        """Get next proxy in rotation"""
        if not self.proxies:
            self.load_proxies()
        
        if not self.proxies:
            return None
        
        # Coba beberapa proxy
        for _ in range(min(5, len(self.proxies))):
            proxy = self.proxies[self.current_index % len(self.proxies)]
            self.current_index += 1
            if proxy not in self.failed_proxies:
                return proxy
        
        return None
    
    def mark_failed(self, proxy):
        """Mark proxy as failed"""
        if proxy:
            self.failed_proxies.add(proxy)
            if proxy in self.proxies:
                self.proxies.remove(proxy)
    
    def mark_success(self, proxy):
        """Mark proxy as success (remove from failed)"""
        if proxy and proxy in self.failed_proxies:
            self.failed_proxies.remove(proxy)
            if proxy not in self.proxies:
                self.proxies.append(proxy)
    
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

# ==================== REQUEST WITH PROXY ====================
class ProxyRequest:
    def __init__(self):
        self.proxy_manager = ProxyManager()
        self.max_retries = 3
    
    def request(self, method, url, **kwargs):
        """Send request with proxy fallback"""
        timeout = kwargs.pop('timeout', 15)
        headers = kwargs.pop('headers', {})
        data = kwargs.pop('data', None)
        json_data = kwargs.pop('json', None)
        cookies = kwargs.pop('cookies', None)
        
        last_error = None
        
        for attempt in range(self.max_retries):
            proxy = self.proxy_manager.get_proxy()
            proxy_dict = self.proxy_manager.get_proxy_dict(proxy)
            
            try:
                req_kwargs = {
                    'headers': headers,
                    'timeout': timeout,
                    'verify': False,
                    'allow_redirects': True,
                }
                
                if cookies:
                    req_kwargs['cookies'] = cookies
                
                if proxy_dict:
                    req_kwargs['proxies'] = proxy_dict
                
                if data is not None:
                    req_kwargs['data'] = data
                elif json_data is not None:
                    req_kwargs['json'] = json_data
                
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
                
                # Kalo response sukses, mark proxy success
                if resp.status_code < 500:
                    self.proxy_manager.mark_success(proxy)
                    return resp
                else:
                    self.proxy_manager.mark_failed(proxy)
                    
            except Exception as e:
                last_error = e
                if proxy:
                    self.proxy_manager.mark_failed(proxy)
                continue
        
        # Fallback tanpa proxy
        try:
            req_kwargs = {
                'headers': headers,
                'timeout': timeout,
                'verify': False,
                'allow_redirects': True,
            }
            if cookies:
                req_kwargs['cookies'] = cookies
            if data is not None:
                req_kwargs['data'] = data
            elif json_data is not None:
                req_kwargs['json'] = json_data
            
            if method.upper() == 'GET':
                return requests.get(url, **req_kwargs)
            elif method.upper() == 'POST':
                return requests.post(url, **req_kwargs)
            else:
                return requests.request(method, url, **req_kwargs)
        except:
            return None

# ==================== SINGLETON ====================
_proxy_request = None

def get_proxy_request():
    global _proxy_request
    if _proxy_request is None:
        _proxy_request = ProxyRequest()
    return _proxy_request

def proxy_request(method, url, **kwargs):
    """Convenience function for proxy request"""
    pr = get_proxy_request()
    return pr.request(method, url, **kwargs)
