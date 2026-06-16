import os
import requests
import time
import json

TOKEN = os.getenv("MAX_TOKEN")

def send_message(chat_id, text):
    """Отправка сообщения через API MAX"""
    url = "https://api.max.ru/v1/messages.send"
    headers = {
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "chat_id": chat_id,
        "text": text
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"📤 Отправлено: {response.status_code} - {response.text[:100]}")
        return response
    except Exception as e:
        print(f"❌ Ошибка отправки: {e}")
        return None

def get_updates():
    """Получение новых сообщений"""
    url = "https://api.max.ru/v1/updates.get"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"📥 Получено: {response.status_code} - {response.text[:200]}")
        if response.status_code == 200:
            data = response.json()
            return data.get("updates", [])
        else:
            print(f"❌ Ошибка HTTP: {response.status_code}")
            return []
    except requests.exceptions.Timeout:
        print("⏰ Таймаут при получении обновлений")
        return []
    except Exception as e:
        print(f"❌ Ошибка получения: {e}")
        return []

print("🚀 БОТ ЗАПУЩЕН!")
print(f"🔑 Токен: {TOKEN[:10]}...{TOKEN[-10:] if TOKEN else 'НЕТ ТОКЕНА!'}")

last_update_id = 0

while True:
    try:
        updates = get_updates()
        for update in updates:
            update_id = update.get("update_id", 0)
            if update_id <= last_update_id:
                continue
            last_update_id = update_id
            
            if "message" in update:
                msg = update["message"]
                chat_id = msg.get("chat", {}).get("id")
                text = msg.get("text", "").strip()
                
                if chat_id:
                    print(f"📨 Сообщение от {chat_id}: {text}")
                    send_message(chat_id, f"✅ Получил: {text}")
    except Exception as e:
        print(f"❌ Ошибка в цикле: {e}")
    
    time.sleep(2)
