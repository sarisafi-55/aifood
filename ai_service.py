import os, json, time

MODEL_DEFAULT = "gemini-3.8-flash"

def _client():
    key = os.getenv("GEMINI_API_KEY", "").strip()
    if not key:
        return None
    from google import genai
    return genai.Client(api_key=key)

def _records(frame, limit):
    if frame is None or frame.empty: return []
    return frame.head(limit).to_dict("records")

def _context(stats, df=None):
    out = {
        "total_sales": round(stats["total_sales"],2), "total_qty": stats["total_qty"],
        "orders": stats["orders"], "avg_order_value": round(stats["avg_order_value"],2),
        "best_menu": stats["best_menu"], "peak_hour": stats["peak_hour"],
        "menu_sales": _records(stats["menu_sales"],50),
        "hourly_sales": _records(stats["hourly"].sort_values("Hour"),24),
        "period_sales": _records(stats["period"],10),
        "category_sales": _records(stats["category"],30),
        "daily_sales": _records(stats["daily"],90),
    }
    if df is not None:
        out["row_count"] = len(df); out["columns"] = list(df.columns)
    return out

def _generate(prompt):
    client = _client()
    if not client: return "ยังไม่ได้ตั้งค่า GEMINI_API_KEY จึงยังใช้ AI ไม่ได้"
    model = os.getenv("GEMINI_MODEL", MODEL_DEFAULT).strip() or MODEL_DEFAULT
    last_error = None
    for attempt in range(3):
        try:
            r = client.models.generate_content(model=model, contents=prompt)
            text = getattr(r, "text", None)
            return text.strip() if text else "AI ไม่ได้ส่งข้อความตอบกลับ กรุณาลองใหม่"
        except Exception as e:
            last_error = e
            msg = str(e)
            if "503" in msg or "UNAVAILABLE" in msg or "high demand" in msg.lower():
                time.sleep(2 + attempt * 2)
                continue
            break
    if last_error and ("503" in str(last_error) or "UNAVAILABLE" in str(last_error)):
        return "ขณะนี้บริการ AI มีผู้ใช้งานจำนวนมาก ระบบลองเชื่อมต่อให้อัตโนมัติแล้ว กรุณารอสักครู่และกดส่งอีกครั้ง"
    return f"AI ยังไม่สามารถตอบได้: {last_error}"

def generate_insight(stats, df=None):
    data=json.dumps(_context(stats,df),ensure_ascii=False,default=str)
    return _generate(f'''คุณคือ Restaurant Business Data Analyst วิเคราะห์เฉพาะ DATA ห้ามสร้างตัวเลขนอกข้อมูล\nDATA:{data}\nตอบภาษาไทย: 1) ภาพรวม 2) เมนู/หมวดหมู่เด่น 3) ช่วงเวลาสำคัญ 4) จุดที่ควรจับตา 5) ข้อเสนอแนะเชิงปฏิบัติ 3 ข้อ''')

def ask_data(stats, df, question):
    data=json.dumps(_context(stats,df),ensure_ascii=False,default=str)
    return _generate(f'''คุณคือผู้ช่วยวิเคราะห์ข้อมูลร้านอาหาร ตอบจาก DATA เท่านั้น หากข้อมูลไม่พอให้บอกว่า ข้อมูลที่อัปโหลดยังไม่เพียงพอสำหรับคำถามนี้ ห้ามสร้างตัวเลข\nDATA:{data}\nคำถาม:{question}\nตอบภาษาไทย โดยตอบคำตอบสำคัญก่อน แล้วอธิบายสั้น ๆ''')
