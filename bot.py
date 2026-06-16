import os
import requests
import time

MAX_TOKEN = os.getenv("MAX_TOKEN")
API_URL = "https://api.max.ru/bot/v1/"

def send_message(chat_id, text):
    """Отправка сообщения через API MAX"""
    url = f"{API_URL}sendMessage"
    payload = {
        "chatId": chat_id,
        "text": text
    }
    headers = {
        "Authorization": f"Bearer {MAX_TOKEN}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=payload, headers=headers)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return None

def get_updates():
    """Получение новых сообщений"""
    url = f"{API_URL}getUpdates"
    headers = {"Authorization": f"Bearer {MAX_TOKEN}"}
    try:
        response = requests.get(url, headers=headers)
        return response.json().get("result", [])
    except Exception as e:
        print(f"Ошибка получения сообщений: {e}")
        return []

# Главный цикл бота
def main():
    print("Бот запущен и работает!")
    processed_ids = set()
    
    while True:
        try:
            updates = get_updates()
            for update in updates:
                # Проверяем, есть ли сообщение
                if "message" in update:
                    msg = update["message"]
                    chat_id = msg.get("chat", {}).get("id")
                    text = msg.get("text", "").lower().strip()
                    
                    # Проверяем, обработано ли уже это сообщение
                    message_id = update.get("update_id")
                    if message_id in processed_ids:
                        continue
                    processed_ids.add(message_id)
                    
                    # Обработка команд
                    if text in ["привет", "здравствуйте", "начать", "/start"]:
                        send_message(chat_id,
                            "Добро пожаловать в Банный Мир Воронеж! 🧖‍♂️\n\n"
                            "Выберите действие:\n"
                            "1 - Записаться в сауну\n"
                            "2 - Посмотреть цены\n"
                            "3 - Адрес и контакты\n"
                            "4 - Акции"
                        )
                    elif text == "1":
                        send_message(chat_id,
                            "📝 Для бронирования укажите:\n\n"
                            "1. Какую сауну? (Финская / Русская / Хаммам)\n"
                            "2. Дата и время (например: 20.06, 19:00)\n"
                            "3. На сколько часов?\n"
                            "4. Ваше имя:\n"
                            "5. Ваш телефон:\n\n"
                            "Менеджер свяжется для подтверждения."
                        )
                    elif text == "2":
                        send_message(chat_id,
                            "💰 Стоимость саун (до 6 человек):\n\n"
                            "• Финская: 1500 ₽/час (будни), 2000 ₽/час (выходные)\n"
                            "• Русская парная: 1800 ₽/час (будни), 2400 ₽/час (выходные)\n"
                            "• Хаммам: 2000 ₽/час (будни), 2600 ₽/час (выходные)\n\n"
                            "➕ Дополнительно:\n"
                            "• Веники: 300 ₽/шт\n"
                            "• Чан с водой: 500 ₽\n\n"
                            "Акция: утренние часы (10:00-14:00) — скидка 15%!"
                        )
                    elif text == "3":
                        send_message(chat_id,
                            "📍 Банный Мир Воронеж\n"
                            "г. Воронеж, ул. Примерная, д. 15\n\n"
                            "🚗 Схема проезда: с Московского проспекта поворот на ул. Ленина\n\n"
                            "📞 +7 (473) 123-45-67\n"
                            "Режим работы: ежедневно 10:00 – 02:00"
                        )
                    elif text == "4":
                        send_message(chat_id,
                            "🎉 Специальные предложения:\n\n"
                            "• Утренние часы (10:00-14:00) — скидка 15%\n"
                            "• Продление часа — скидка 20%\n"
                            "• Приведи друга — скидка 10% на следующий визит"
                        )
                    else:
                        send_message(chat_id,
                            "Не понял Вас 😊\n\n"
                            "Напишите:\n"
                            "1 - Записаться\n"
                            "2 - Цены\n"
                            "3 - Адрес\n"
                            "4 - Акции"
                        )
        except Exception as e:
            print(f"Ошибка в цикле: {e}")
        
        time.sleep(1)  # Пауза 1 секунда

if __name__ == '__main__':
    main()
