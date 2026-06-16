import os
import requests
import time

TOKEN = os.getenv("MAX_TOKEN")

def send_message(chat_id, text):
    url = "https://max.ru"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        print("ОТВЕТ:", r.status_code, r.text)
    except Exception as e:
        print("ОШИБКА ОТПРАВКИ:", e)

def get_updates(offset=0):
    url = "https://max.ru"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    # Передаем offset, чтобы сервер не возвращал старые сообщения
    params = {"offset": offset}
    try:
        r = requests.get(url, headers=headers, params=params, timeout=10)
        print("ПОЛУЧЕНО:", r.status_code, r.text[:200])
        if r.status_code == 200:
            return r.json().get("updates", [])
        else:
            print(f"Ошибка API: код {r.status_code}")
    except Exception as e:
        print("ОШИБКА ПОЛУЧЕНИЯ:", e)
    return []

print("🚀 БОТ ЗАПУЩЕН!")
last_id = 0

while True:
    try:
        # Запрашиваем обновления, начиная со следующего после last_id
        updates = get_updates(offset=last_id + 1)
        
        for u in updates:
            uid = u.get("update_id", 0)
            if uid <= last_id:
                continue
            last_id = uid  # Фиксируем, что это обновление прочитано
            
            msg = u.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")
            
            if chat_id:
                send_message(chat_id, f"✅ Получил: {text}")
                
    except Exception as e:
        print("ОШИБКА ЦИКЛА:", e)
        
    time.sleep(2)
