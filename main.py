from flask import Flask, request, Response
from datetime import datetime
import json
import requests

# === אתחול Flask ===
app = Flask(__name__)

# === הגדרות Supabase ===
SUPABASE_URL = "https://ilmtxjzxbrfbfdlgjpkh.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlsbXR4anp4YnJmYmZkbGdqcGtoIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1Nzc5ODQ4MCwiZXhwIjoyMDczMzc0NDgwfQ.af1Pzuyk8SwhrLFQY0ESy5WtjX5orKmonZf8RKVipsI"
USERS_TABLE = "משתמשים"  # שם הטבלה בסופבייס

# === פונקציה לשמירת משתמש חדש ===
def save_user(phone_number):
    """
    שומר משתמש חדש בטבלת 'משתמשים'
    """
    url = f"{SUPABASE_URL}/rest/v1/{USERS_TABLE}"
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }

    payload = {
        "phone_number": str(phone_number),              # המספר של המאזין
        "joined_at": datetime.utcnow().isoformat(),     # תאריך הצטרפות ב-UTC
        "nikud": 5                                      # תמיד חמש
    }

    print(f"📤 שולח ל-Supabase (משתמשים): {json.dumps(payload, ensure_ascii=False)}")
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.status_code, response.text

# === נקודת API לקליטת הבקשות מימות המשיח ===
@app.route("/user_join", methods=["GET"])
def user_join():
    """
    כל פעם שמאזין נכנס לשלוחה, ימות המשיח שולחים בקשה לכאן
    פרמטרים חשובים:
    - ApiPhone: מספר הטלפון של המאזין
    """
    phone = request.args.get("ApiPhone")

    print("========================================")
    print("📞 בקשה התקבלה מימות המשיח")
    print(f"    ApiPhone = '{phone}'")

    if not phone:
        print("❌ לא התקבל מספר טלפון - פעולה בוטלה")
        return Response("missing phone number", mimetype="text/plain; charset=utf-8")

    # שמירת המידע ב-Supabase
    status_code, supabase_response = save_user(phone)

    if status_code == 201:
        print("✅ נשמר בהצלחה בטבלה 'משתמשים'")
    else:
        print(f"❌ שגיאה בשמירה ל-Supabase (סטטוס {status_code}): {supabase_response}")

    print("========================================")

    # החזרת תגובה לימות המשיח
    return Response("ok", mimetype="text/plain; charset=utf-8")

# === הרצת השרת ===
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))  # פורט נפרד מהקוד הראשי
    print(f"🚀 השרת עלה בהצלחה ומאזין על פורט {port}...")
    app.run(host="0.0.0.0", port=port)
