from flask import Flask, request, abort

app = Flask(__name__)

# Basit saldırı kalıpları
SQL_INJECTION_PATTERNS = [
    "select", "union", "insert", "update", "delete", "drop", "--", ";", "'"
]

XSS_PATTERNS = [
    "<script>", "</script>", "javascript:", "onerror", "onload"
]

# Güvenlik duvarı kontrol fonksiyonu
def waf_check():
    # İstek parametrelerini kontrol et
    for key, value in request.args.items():
        if any(pattern in value.lower() for pattern in SQL_INJECTION_PATTERNS):
            abort(403, description="SQL Injection attempt detected")
        if any(pattern in value.lower() for pattern in XSS_PATTERNS):
            abort(403, description="XSS attempt detected")

    # İstek gövdesini kontrol et
    if request.data:
        data = request.data.decode('utf-8').lower()
        if any(pattern in data for pattern in SQL_INJECTION_PATTERNS):
            abort(403, description="SQL Injection attempt detected")
        if any(pattern in data for pattern in XSS_PATTERNS):
            abort(403, description="XSS attempt detected")

# Tüm isteklerde güvenlik duvarı kontrolünü çalıştır
@app.before_request
def before_request():
    waf_check()

@app.route('/')
def index():
    return "Welcome to the secure web application!"

@app.route('/data', methods=['POST'])
def data():
    return "Data received securely!"

if __name__ == '__main__':
    app.run(debug=True)
