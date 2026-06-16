import os
import requests
import time

TOKEN = os.getenv("MAX_TOKEN")

def send_message(chat_id, text):
    url = "https://api.max.ru/v1/messages.send"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        print("ОТВЕТ:", r.status_code, r.text)
    except Exception as e:
        print("ОШИБКА:", e)

def get_updates():
    url = "https://api.max.ru/v1/updates.get"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print("ПОЛУЧЕНО:", r.status_code, r.text[:200])
        if r.status_code == 200:
            return r.json().get("updates", [])
    except Exception as e:
        print("ОШИБКА ПОЛУЧЕНИЯ:", e)
    return []

print("🚀 БОТ ЗАПУЩЕН!")
last_id = 0

while True:
    try:
        updates = get_updates()
        for u in updates:
            uid = u.get("update_id", 0)
            if uid <= last_id:
                continue
            last_id = uid
            msg = u.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")
            if chat_id:
                send_message(chat_id, f"✅ Получил: {text}")
    except Exception as e:
        print("ОШИБКА ЦИКЛА:", e)
    time.sleep(2)
