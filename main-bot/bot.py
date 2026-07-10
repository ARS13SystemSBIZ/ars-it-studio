import os
import telebot
from telebot import types
from flask import Flask, request
from dotenv import load_dotenv

# Читаем секретный токен из .env файла
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
YOUR_CHAT_ID = 6240010880  

bot = telebot.TeleBot(TOKEN)
user_data = {}

PRICES = {
    "type_site": 250, "type_bot": 180,
    "level_easy": 70, "level_hard": 300,
    "addon_yes": 120, "addon_no": 0
}

# Создаём мини-веб-сервер Flask
server = Flask(__name__)

# ================= ТЕКСТОВЫЕ КОМАНДЫ БОТА =================
@bot.message_handler(commands=['start'])
def start_funnel(message):
    chat_id = message.chat.id
    user_data[chat_id] = {'mode': 'calc', 'price_steps': {}, 'from_portfolio': False}
    
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📊 Рассчитать стоимость проекта", callback_data="main_calc"),
        types.InlineKeyboardButton("💼 Посмотреть наше портфолио", callback_data="main_portfolio")
    )
    bot.send_message(chat_id, "Здравствуйте! Добро пожаловать в IT-студию Арсения. 👋\n\nМы создаем премиальных чат-ботов и продающие веб-сайты для автоматизации вашего бизнеса.\n\nВыберите интересующий вас раздел ниже 👇", reply_markup=markup)

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(message.chat.id, "🎯 *Служба поддержки IT-студии Арсения*\n\nЕсли у вас возникли вопросы по расчету стоимости или вам нужно индивидуальное ТЗ, напишите мне напрямую: @ARider13", parse_mode="Markdown")


# ================= ОБРАБОТКА ИНЛАЙН КНОПОК (CALLBACK) =================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    chat_id = call.message.chat.id
    data = call.data
    
    if chat_id not in user_data:
        user_data[chat_id] = {'mode': 'calc', 'price_steps': {}, 'from_portfolio': False}

    # ГЛАВНЫЙ БЛОК ПОРТФОЛИО
    if data == "main_portfolio":
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("☕ Кейс: Бот-Кофейня 'Coffee Express'", url="https://t.me/ars_coffee_demo_bot"),
            types.InlineKeyboardButton("🧮 Кейс: Интерактивный калькулятор", callback_data="case_calc"),
            types.InlineKeyboardButton("🖥️ Кейс: Личный сайт-визитка", callback_data="case_site"),
            types.InlineKeyboardButton("🌿 Кейс: Сайт 'Green Luxury'", callback_data="case_landscape"),
            types.InlineKeyboardButton("⭐️ Отзывы и Гарантии студии", callback_data="case_reviews"),
            types.InlineKeyboardButton("💬 Связаться с Арсением напрямую", url="https://t.me/ARider13"),
            types.InlineKeyboardButton("🔙 Вернуться в главное меню", callback_data="back_to_main")
        )
        bot.edit_message_text("💼 *Портфолио IT-студии Арсения*\n\nНиже представлены наши готовые решения для автоматизации бизнеса и лидогенерации. Нажмите на любой кейс, чтобы изучить его детально или протестировать:", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # КЕЙС 1: КАЛЬКУЛЯТОР
    elif data == "case_calc":
        markup = types.InlineKeyboardMarkup()
        markup.row(
            types.InlineKeyboardButton("🚀 Запустить тест-драйв", callback_data="portfolio_calc_start"),
            types.InlineKeyboardButton("🔙 Назад в портфолио", callback_data="main_portfolio")
        )
        case_text = (
            "🧮 *Кейс: Интерактивный калькулятор услуг*\n\n"
            "• *Для кого:* Сфера услуг, фрилансеры, онлайн-школы, строительные компании.\n"
            "• *Какую боль решает:* Избавляет менеджеров от рутинных расчетов, заменяет скучные прайс-листы интерактивным игровым опросом.\n"
            "• *Бэкэнд-логика:* Динамический подсчет сметы в реальном времени, автоматическая конвертация валюты в $, перехват команд и мгновенная генерация карточки лида владельцу.\n"
            "• *Результат:* Поднимает конверсию из посетителя в заявку на 40%."
        )
        bot.edit_message_text(case_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # КЕЙС 2: ЛИЧНЫЙ САЙТ
    elif data == "case_site":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Назад в портфолио", callback_data="main_portfolio"))
        
        site_text = (
            "🖥️ *Кейс: Адаптивный сайт-визитка IT-студии*\n\n"
            "• *Для кого:* Личный бренд разработчика, эксперты, digital-агентства.\n"
            "• *Дизайн:* Трендовый Dark Mode (тёмная тема) с neon-голубыми элементами.\n"
            "• *Функционал:* Написание чистого семантического кода HTML5 и CSS3. Полная адаптивность: сайт идеально подстраивается под экраны любых смартфонов, планшетов и 4К-мониторов.\n"
            "• *Маркетинг:* Интегрирована яркая интерактивная кнопка захвата внимания с плавным hover-эффектом для перелива трафика в Telegram-ботов."
        )
        bot.edit_message_text(site_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # КЕЙС 3: ЛАНДШАФТНЫЙ ДИЗАЙН
    elif data == "case_landscape":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Назад в портфолио", callback_data="main_portfolio"))
        
        landscape_text = (
            "🌿 *Кейс: Премиум-сайт для студии 'Green Luxury'*\n\n"
            "• *Для кого:* Ландшафтные архитекторы, дизайн-студии, элитная недвижимость, B2C сектор с высоким чеком.\n"
            "• *Визуальное решение:* Роскошный полноэкранный фоновый баннер (европейское поместье-замок с аллеями и туями). Использование классической благородной типографики Georgia.\n"
            "• *Технологии:* Интерактивная CSS-сетка услуг (Services Grid). Карточки используют технологию матового стекла (rgba-прозрачность) и плавно приподнимаются на 3D-эффекте при наведении курсора.\n"
            "• *Результат:* Создает премиальный образ бренда, идеально подчеркивает элитарность услуг и обосновывает высокий чек компании."
        )
        bot.edit_message_text(landscape_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # РАЗДЕЛ: ОТЗЫВЫ И ГАРАНТИИ
    elif data == "case_reviews":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙 Назад в портфолио", callback_data="main_portfolio"))
        
        reviews_text = (
            "⭐️ *Гарантии и Отзывы IT-студии Арсения*\n\n"
            "• *Безопасная сделка:* Мы дорожим репутацией и работаем строго по официальному договору. Все этапы, сроки и фиксированная стоимость прописываются юридически.\n"
            "• *Пошаговая оплата:* Никаких 100% предоплат 'вслепую'. Оплата разбивается на комфортные этапы 50/50. Вы платите за реальный, проверенный результат.\n"
            "• *Техподдержка 14 дней:* После запуска сайта или бота мы бесплатно сопровождаем ваш проект, исправляем любые баги и помогаем вашей команде разобраться в системе.\n\n"
            "💬 Хотите изучить отзывы наших реальных клиентов или обсудить ваш проект индивидуально? Нажмите кнопку связи с разработчиком в меню портфолио!"
        )
        bot.edit_message_text(reviews_text, chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # НАВИГАЦИОННЫЕ КНОПКИ
    elif data == "back_to_main": 
        bot.delete_message(chat_id, call.message.message_id)
        start_funnel(call.message)
    elif data == "portfolio_calc_start": 
        user_data[chat_id]['from_portfolio'] = True
        run_calculator_init(chat_id, call.message.message_id)
    elif data == "main_calc": 
        user_data[chat_id]['from_portfolio'] = False
        run_calculator_init(chat_id, call.message.message_id)
    elif data in ["type_site", "type_bot", "level_easy", "level_hard", "addon_yes", "addon_no", "start_order"]: 
        handle_calculator_steps(chat_id, data, call.message.message_id)

# ================= ВНУТРЕННИЕ СЛУЖЕБНЫЕ ФУНКЦИИ =================
def handle_calculator_steps(chat_id, data, message_id):
    if data in ["type_site", "type_bot"]:
        user_data[chat_id]['price_steps']['type'] = data
        type_text = "Веб-сайт 🌐" if data == "type_site" else "Чат-бот 🤖"
        bot.edit_message_text(f"Что именно вам необходимо разработать?\n↳ *Выбрано:* {type_text}", chat_id, message_id, parse_mode="Markdown")
        
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("⚡ Простой (Базовый)", callback_data="level_easy"), 
                   types.InlineKeyboardButton("🔥 Сложный (С интеграциями)", callback_data="level_hard"))
        bot.send_message(chat_id, "Какая сложность и функционал планируются?", reply_markup=markup)

    elif data in ["level_easy", "level_hard"]:
        user_data[chat_id]['price_steps']['level'] = data
        level_text = "Простой (Базовый) ⚡" if data == "level_easy" else "Сложный (С интеграциями) 🔥"
        bot.edit_message_text(f"Какая сложность и функционал планируются?\n↳ *Выбрано:* {level_text}", chat_id, message_id, parse_mode="Markdown")
        
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("✅ Да, нужно", callback_data="addon_yes"), 
                   types.InlineKeyboardButton("❌ Нет, спасибо", callback_data="addon_no"))
        bot.send_message(chat_id, "Требуется ли индивидуальный дизайн и маркетинговая настройка?", reply_markup=markup)

    elif data in ["addon_yes", "addon_no"]:
        user_data[chat_id]['price_steps']['addon'] = data
        addon_text = "Да, нужно индивидуальный дизайн ✅" if data == "addon_yes" else "Нет, спасибо ❌"
        bot.edit_message_text(f"Требуется ли индивидуальный дизайн и маркетинговая настройка?\n↳ *Выбрано:* {addon_text}", chat_id, message_id, parse_mode="Markdown")
        
        steps = user_data[chat_id]['price_steps']
        total_price = PRICES[steps['type']] + PRICES[steps['level']] + PRICES[steps['addon']]
        
        # Автоматический расчет скидки за сложный проект
        discount = 0
        if steps['level'] == "level_hard":
            discount = 50
            total_price -= discount
            
        user_data[chat_id]['calculated_price'] = total_price
        
        type_conf = "Веб-сайт" if steps['type'] == "type_site" else "Чат-бот"
        level_conf = "Простой" if steps['level'] == "level_easy" else "Сложный"
        addon_conf = "С дизайном" if steps['addon'] == "addon_yes" else "Без дизайна"
        user_data[chat_id]['config_text'] = f"{type_conf} ({level_conf}, {addon_conf})"
        
        # Формируем красивый текст чека с уведомлением о скидке
        result_text = (
            f"📊 *Расчет стоимости готов!*\n\n"
            f"• Тип проекта: {type_conf}\n"
            f"• Сложность: {level_conf}\n"
            f"• Опции: {addon_conf}\n\n"
        )
        
        if discount > 0:
            result_text += f"🔥 *Вам доступна скидка за сложность:* -${discount}\n\n"
            
        result_text += f"💰 Итоговая стоимость: *${total_price}*\n\nВы можете забронировать эту стоимость прямо сейчас. Нажмите кнопку ниже 👇"
        
        markup = types.InlineKeyboardMarkup()
        markup.row(types.InlineKeyboardButton("🚀 Оформить заказ по этой цене", callback_data="start_order"))
        bot.send_message(chat_id, result_text, parse_mode="Markdown", reply_markup=markup)

    elif data == "start_order":
        user_data[chat_id]['mode'] = 'order'
        bot.edit_message_text(f"📊 *Расчет стоимости готов!*\n\n💰 Ориентировочная стоимость: *${user_data[chat_id]['calculated_price']}*\n\n↳ *Статус:* Начинаем оформление заказа... ⏳", chat_id, message_id, parse_mode="Markdown")
        msg = bot.send_message(chat_id, "Как к вам обращаться? Введите ваше имя:")
        bot.register_next_step_handler(msg, get_client_name)

def run_calculator_init(chat_id, message_id):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("🌐 Веб-сайт", callback_data="type_site"), 
               types.InlineKeyboardButton("🤖 Чат-бот", callback_data="type_bot"))
    if user_data[chat_id].get('from_portfolio'):
        welcome_text = "🔥 *ТЕСТ-ДРАЙВ КЕЙСА:*\nВы запустили интерактивную демонстрацию калькулятора. Попробуйте пощёлкать кнопки, чтобы увидеть бэкенд-логику в действии!\n\nЧто именно необходимо разработать? Выберите тип проекта:"
    else:
        welcome_text = "Что именно вам необходимо разработать? Выберите тип проекта:"
    bot.edit_message_text(welcome_text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

# ================= ПОШАГОВЫЙ СБОР КОНТАКТОВ =================
def get_client_name(message):
    chat_id = message.chat.id
    if message.text in ['/start']: 
        start_funnel(message)
        return
    user_data[chat_id]['name'] = message.text
    msg = bot.send_message(chat_id, f"Приятно познакомиться, {message.text}! 👋\n\nВведите ваш номер телефона или юзернейм для связи:")
    bot.register_next_step_handler(msg, get_client_contact)

def get_client_contact(message):
    chat_id = message.chat.id
    if message.text in ['/start']: 
        start_funnel(message)
        return
    user_data[chat_id]['contact'] = message.text
    msg = bot.send_message(chat_id, "Оставьте комментарий к заказу или ваши пожелания (если вопросов нет, отправьте дефис «-»):")
    bot.register_next_step_handler(msg, get_client_task)

def get_client_task(message):
    chat_id = message.chat.id
    if message.text in ['/start']: 
        start_funnel(message)
        return

    name = user_data[chat_id]['name']
    contact = user_data[chat_id]['contact']
    comment = message.text
    config = user_data[chat_id].get('config_text', 'Не рассчитано')
    final_price = user_data[chat_id].get('calculated_price', 0)
    username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"
    
    lead_message = (
        f"🔥 *НОВЫЙ ГОРЯЧИЙ КЛИЕНТ ИЗ ВОРОНКИ!* 🔥\n\n"
        f"👤 *Имя:* {name}\n"
        f"📞 *Контакты:* {contact}\n"
        f"💬 *Аккаунт ТГ:* {username}\n\n"
        f"🛠️ *Что выбрал:* {config}\n"
        f"💰 *Рассчитанная цена:* ${final_price}\n"
        f"📋 *Комментарий:* {comment}"
    )
    bot.send_message(YOUR_CHAT_ID, lead_message, parse_mode="Markdown")
    bot.send_message(chat_id, f"Спасибо! Ваша конфигурация на сумму *${final_price}* и контакты успешно переданы. Арсений свяжется с вами в течение 15 минут! 🤝", parse_mode="Markdown")
    del user_data[chat_id]

# Автоматическая настройка синего меню команд
bot.set_my_commands([
    types.BotCommand("start", "🚀 Запустить главное меню студии"),
    types.BotCommand("help", "🎯 Связаться со службой поддержки")
])

# ================= WEBHOOK (для сервера) =================
@server.route("/webhook", methods=["POST"])
def webhook():
    if request.headers.get("content-type") == "application/json":
        json_string = request.get_data().decode("utf-8")
        update = types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "ok", 200
    return "error", 400

if __name__ == "__main__":
    # Проверяем, есть ли переменная WEBHOOK_URL в .env
    WEBHOOK_URL = os.getenv("WEBHOOK_URL")

    if WEBHOOK_URL:
        # Режим WEBHOOK (для сервера)
        print(f"🚀 Бот запущен через Webhook: {WEBHOOK_URL}")
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        port = int(os.environ.get("PORT", 5000))
        server.run(host="0.0.0.0", port=port)
    else:
        # Режим POLLING (для локального теста)
        print(" Бот запущен через Polling (локальный режим)")
        bot.infinity_polling()
