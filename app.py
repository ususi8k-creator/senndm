from flask import Flask, render_template_string, request, jsonify
from twilio.rest import Client

app = Flask(__name__)

# --- إعدادات Twilio الخاصة بك ---
ACCOUNT_SID = 'AC13a7387376fe9394532a6f7aa4c1f06e'
AUTH_TOKEN = '9f8ea374ff149e72606884b640044b9d'  # استبدل هذا بالرمز السري الحقيقي
TWILIO_NUMBER = '+14343035557'

client = Client(ACCOUNT_SID, AUTH_TOKEN)

# --- واجهة المستخدم (HTML/CSS) ---
HTML_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMS PRO | Dashboard</title>
    <style>
        body { background: #f8fafc; font-family: 'Segoe UI', Tahoma, sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 40px; border-radius: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.05); width: 360px; text-align: center; border: 1px solid #f1f5f9; }
        .icon-box { background: #eff6ff; width: 70px; height: 70px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 20px; font-size: 30px; }
        h2 { color: #1e293b; font-size: 24px; margin-bottom: 5px; }
        p { color: #94a3b8; font-size: 13px; margin-bottom: 30px; }
        .group { text-align: right; margin-bottom: 15px; }
        label { display: block; font-size: 12px; font-weight: 600; color: #64748b; margin-bottom: 8px; }
        input { width: 100%; padding: 14px; border: 1.5px solid #e2e8f0; border-radius: 12px; box-sizing: border-box; outline: none; transition: 0.3s; font-size: 15px; background: #fff; text-align: left; direction: ltr; }
        input:focus { border-color: #6366f1; background: #f5f7ff; }
        button { width: 100%; padding: 15px; background: #6366f1; border: none; border-radius: 15px; color: white; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s; margin-top: 10px; box-shadow: 0 4px 12px rgba(99, 102, 241, 0.2); }
        button:hover { background: #4f46e5; transform: translateY(-2px); }
        #status { margin-top: 20px; font-size: 12px; color: #64748b; border-top: 1px solid #f1f5f9; padding-top: 15px; line-height: 1.6; }
    </style>
</head>
<body>
    <div class="card">
        <div class="icon-box">📲</div>
        <h2>إرسال OTP ذكي</h2>
        <p>بوابة إرسال الرسائل عبر Twilio API</p>
        <div class="group">
            <label>رقم الهاتف (مع مفتاح الدولة +964)</label>
            <input type="text" id="phone" placeholder="+9647700000000">
        </div>
        <div class="group">
            <label>نص الرسالة أو كود التحقق</label>
            <input type="text" id="msg" style="text-align: right; direction: rtl;" placeholder="رمز التحقق الخاص بك هو: 1234">
        </div>
        <button onclick="send()">إرسال الرسالة الآن 🚀</button>
        <div id="status">حالة السيرفر: جاهز للعمل</div>
    </div>

    <script>
        async function send() {
            const phone = document.getElementById('phone').value;
            const msg = document.getElementById('msg').value;
            const status = document.getElementById('status');
            
            if(!phone || !msg) return alert("يرجى إكمال البيانات");
            
            status.innerText = "⏳ جاري المعالجة عبر Twilio...";
            
            try {
                const r = await fetch('/send_sms', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({phone, msg})
                });
                const res = await r.json();
                if(res.status === 'success') {
                    status.innerHTML = "<b style='color:green;'>✅ تم الإرسال بنجاح!</b><br>SID: " + res.sid;
                } else {
                    status.innerHTML = "<b style='color:red;'>❌ فشل الإرسال:</b><br>" + res.error;
                }
            } catch (e) {
                status.innerText = "❌ خطأ في الاتصال بالسيرفر";
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
    
    try:
        # تنفيذ عملية الإرسال الحقيقية
        message = client.messages.create(
            body=msg,
            from_=TWILIO_NUMBER,
            to=phone
        )
        return jsonify({"status": "success", "sid": message.sid})
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)})

if __name__ == '__main__':
    app.run()
