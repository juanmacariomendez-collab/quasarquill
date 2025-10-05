import os, requests
TOKEN = os.environ.get("TELEGRAM_TOKEN","")
CHAT  = os.environ.get("TELEGRAM_CHAT_ID","")
def notify(msg: str):
    if not TOKEN or not CHAT:
        print("Notify skipped: TELEGRAM_TOKEN or TELEGRAM_CHAT_ID not set")
        return
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT, "text": f"[angela quasarquill] {msg}"}, timeout=10)
    except Exception as e:
        print("Notify exception:", e)
