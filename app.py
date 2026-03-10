from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# واجهة مستخدم نظيفة تشبه الرابط الذي أرسلته
HTML_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mersal SMS Pro</title>
    <style>
        body { background: #f8f9fa; font-family: sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); width: 340px; text-align: center; }
        h2 { color: #333; font-size: 1.4rem; margin-bottom: 20px; }
        input, textarea { width: 100%; padding: 12px; margin-bottom: 15px; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; font-size: 14px; }
        button { width: 100%; padding: 12px; background: #007bff; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; font-size: 16px; }
        #status { margin-top: 15px; font-size: 13px; color: #666; }
    </style>
</head>
<body>
    <div class="card">
        <h2>بوابة مرسال الذكية</h2>
        <input type="text" id="phone" placeholder="رقم الهاتف: 96477xxxxxxxx">
        <textarea id="msg" rows="3" placeholder="نص الرسالة..."></textarea>
        <button onclick="send()">إرسال الآن 🚀</button>
        <div id="status">جاهز للعمل</div>
    </div>
    <script>
        async function send() {
            const phone = document.getElementById('phone').value;
            const msg = document.getElementById('msg').value;
            const status = document.getElementById('status');
            
            if(!phone || !msg) return alert("يرجى إكمال البيانات");
            
            status.innerText = "⏳ جاري الإرسال عبر السيرفر...";
            
            try {
                const r = await fetch('/send_sms', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({phone, msg})
                });
                const res = await r.json();
                status.innerText = "رد السيرفر: " + (res.message || res.error);
            } catch (e) {
                status.innerText = "❌ فشل الاتصال بالسيرفر الخاص بك";
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_UI)

@app.route('/send_sms', methods=['POST'])
def send_sms():
    data = request.json
    phone = data.get('phone')
    msg = data.get('msg')
    
    # --- إعدادات بوابة مرسال (ضع بياناتك هنا) ---
    API_KEY = "ضغ_مفتاحك_هنا"
    SENDER = "اسم_المرسل"
    # ------------------------------------------

    api_url = f"https://api.mersal.com/v1/send" 
    payload = {
        "api_key": API_KEY,
        "sender": SENDER,
        "number": phone,
        "message": msg
    }

    try:
        # السيرفر يرسل الطلب مباشرة دون قيود المتصفح
        r = requests.post(api_url, json=payload, timeout=10)
        return jsonify(r.json())
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run()
