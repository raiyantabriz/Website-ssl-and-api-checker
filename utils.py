import socket
import ssl
import dns.resolver
import requests
from bs4 import BeautifulSoup

def check_ssl(domain):
    try:
        ctx = ssl.create_default_context()
        with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
            s.settimeout(3)
            s.connect((domain, 443))
            cert = s.getpeercert()
            return f"✅ SSL is valid. Issuer: {cert['issuer'][0][0][1]}"
    except Exception as e:
        return f"❌ SSL check failed: {str(e)}"

def get_dns_info(domain):
    try:
        ip = socket.gethostbyname(domain)
        dns_info = dns.resolver.resolve(domain, 'A')
        return f"IP: {ip}, DNS: {[rdata.to_text() for rdata in dns_info]}"
    except Exception as e:
        return f"❌ DNS lookup failed: {str(e)}"

def get_site_title(url):
    try:
        res = requests.get(url, timeout=5)
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.title.string if soup.title else 'No Title Found'
        return f"Title: {title}"
    except Exception as e:
        return f"❌ Site title fetch failed: {str(e)}"
