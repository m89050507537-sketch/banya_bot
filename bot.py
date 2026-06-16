import os
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

TOKEN = os.getenv("MAX_TOKEN")
BASE_URL = "https://max.ru"

def send_message(chat_id, text):
    url = f"{BASE_URL}/messages"
    headers = {"Authorization": f"Bearer {TOKEN}"}
    data = {"chat_id": chat_id, "text": text}
    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        print("ОТВЕТ ОТПРАВКИ:", r.status_code, r.text[:200])
    except Exception as e:
        print("ОШИБКА ОТПРАВКИ:", e)

# Эндпоинт, на который Max будет присылать сообщения
@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.get_json()
        print("ПОЛУЧЕНО УВЕДОМЛЕНИЕ:", data)
        
        # Разбираем структуру обновления от Max
        if data and "message" in data:
            msg = data.get("message", {})
            chat_id = msg.get("chat", {}).get("id")
            text = msg.get("text", "")
            
            if chat_id:
                send_message(chat_id, f"✅ Получил через Webhook: {text}")
                
    except Exception as e:
        print("Ошибка обработки вебхука:", e)
        
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    print("🚀 ВЕБХУК-БОТ ЗАПУЩЕН НА ПОРТУ 8080!")
    # Платформа Bothost ожидает, что приложение слушает порт 8080
    app.run(host="0.0.0.0", port=8080)
