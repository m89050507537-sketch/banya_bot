import os
import requests
import time

TOKEN = os.getenv("MAX_TOKEN")
# Базовый URL официального API MAX
BASE_URL = "https://platform-api.max.ru"

def send_message(chat_id, text):
    url = f"{BASE_URL}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    # Параметры могут передаваться как в JSON, так и в params в зависимости от версии
    data = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        print("ОТВЕТ ОТПРАВКИ:", r.status_code, r.text[:200])
    except Exception as e:
        print("ОШИБКА ОТПРАВКИ:", e)

def get_updates(offset=0):
    # Корректный эндпоинт получения обновлений Long Polling в MAX API
    url = f"{BASE_URL}/subscriptions/updates"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    params = {"offset": offset}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        if r.status_code == 200:
            return r.json().get("updates", [])
        else:
            print(f"ПОЛУЧЕНО: {r.status_code}. Проверьте токен или эндпоинт.")
    except Exception as e:
        print("ОШИБКА ПОЛУЧЕНИЯ:", e)
    return []

print("🚀 БОТ ЗАПУЩЕН С ПРАВИЛЬНЫМИ URL!")
last_id = 0

while True:
    try:
        updates = get_updates(offset=last_id + 1)
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
