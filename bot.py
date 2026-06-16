import os
from max_api_client_python import MaxApiClient

MAX_TOKEN = os.getenv("MAX_TOKEN")

# Инициализация клиента
client = MaxApiClient(token=MAX_TOKEN)

def send_message(chat_id, text):
    """Отправка сообщения через официальный SDK"""
    try:
        response = client.messages.send(
            chat_id=chat_id,
            text=text
        )
        return response
    except Exception as e:
        print(f"Ошибка отправки: {e}")
        return None

def get_updates():
    """Получение новых сообщений через официальный SDK"""
    try:
        updates = client.updates.get()
        return updates.get("updates", [])
    except Exception as e:
        print(f"Ошибка получения: {e}")
        return []

def main():
    print("✅ Бот Банный Мир Воронеж запущен!")
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
                    text = msg.get("text", "").lower().strip()
                    
                    if not chat_id:
                        continue
                    
                    # Приветствие
                    if text in ["привет", "здравствуйте", "начать", "/start"]:
                        send_message(chat_id,
                            "Добро пожаловать в Банный Мир Воронеж! 🧖‍♂️\n\n"
                            "Выберите действие:\n"
                            "1 - Записаться в сауну\n"
                            "2 - Посмотреть цены\n"
                            "3 - Адрес и контакты\n"
                            "4 - Акции"
                        )
                    # Запись
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
                    # Цены
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
                    # Адрес
                    elif text == "3":
                        send_message(chat_id,
                            "📍 Банный Мир Воронеж\n"
                            "г. Воронеж, ул. Примерная, д. 15\n\n"
                            "🚗 Схема проезда: с Московского проспекта поворот на ул. Ленина\n\n"
                            "📞 +7 (473) 123-45-67\n"
                            "Режим работы: ежедневно 10:00 – 02:00"
                        )
                    # Акции
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
            import time
            time.sleep(5)
        
        import time
        time.sleep(1)

if __name__ == "__main__":
    main()
