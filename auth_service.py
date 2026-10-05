import os
import requests

BASE = "https://identitytoolkit.googleapis.com/v1/accounts"

def firebase_enabled():
    return bool(os.getenv("FIREBASE_API_KEY"))

def _call(action, email, password):
    key = os.getenv("FIREBASE_API_KEY")
    if not key:
        return False, "ยังไม่ได้ตั้งค่า FIREBASE_API_KEY"
    try:
        r = requests.post(f"{BASE}:{action}?key={key}", json={"email": email, "password": password, "returnSecureToken": True}, timeout=15)
        data = r.json()
        if r.ok:
            return True, data
        code = data.get("error", {}).get("message", "AUTH_ERROR")
        friendly = {
            "EMAIL_EXISTS":"อีเมลนี้ถูกลงทะเบียนแล้ว", "INVALID_LOGIN_CREDENTIALS":"อีเมลหรือรหัสผ่านไม่ถูกต้อง",
            "WEAK_PASSWORD : Password should be at least 6 characters":"รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร",
            "INVALID_EMAIL":"รูปแบบอีเมลไม่ถูกต้อง", "MISSING_PASSWORD":"กรุณากรอกรหัสผ่าน"
        }.get(code, code)
        return False, friendly
    except Exception as e:
        return False, f"เชื่อมต่อ Firebase ไม่สำเร็จ: {e}"

def login(email, password): return _call("signInWithPassword", email, password)
def register(email, password): return _call("signUp", email, password)
