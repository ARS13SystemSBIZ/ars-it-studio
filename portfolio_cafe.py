import telebot
from telebot import types

TOKEN = '8900991692:AAF9CQBPbNMYHwgYvurfpFuGSCv2CsNhnuI'
YOUR_CHAT_ID = 6240010880  

bot = telebot.TeleBot(TOKEN)
user_states = {}

# 1. ПРАЙС-ЛИСТ КОФЕ
MENU = {
    "espresso": {"name": "Эспрессо ☕", "price": 2.0},
    "americano": {"name": "Американо ☕", "price": 2.5},
    "cappuccino": {"name": "Капучино 🥛", "price": 3.5},
    "latte": {"name": "Латте Макиато 🥛", "price": 4.0},
    "flatwhite": {"name": "Флэт Уайт ☕🥛", "price": 3.8},
    "raf": {"name": "Раф Кофе 🍯✨", "price": 4.5}
}

# 2. РАЗМЕРЫ СТАКАНОВ (Только на вынос!)
SIZES = {
    "size_m": {"name": "Средний (M) 🔸", "price": 0.0},
    "size_l": {"name": "Большой (L) ⬆️", "price": 0.5},
    "size_xl": {"name": "Мега (XL) 🔥", "price": 1.0}
}

# 3. АССОРТИМЕНТ СИРОПОВ
SYRUPS = {
    "no": {"name": "Без сиропа ❌", "price": 0.0},
    "vanilla": {"name": "Ванильный 🍦", "price": 0.5},
    "caramel": {"name": "Карамельный 🍯", "price": 0.5},
    "coconut": {"name": "Кокосовый 🥥", "price": 0.5},
    "hazelnut": {"name": "Ореховый 🌰", "price": 0.6}
}

# 4. ФОРМАТ ОБСЛУЖИВАНИЯ
SERVE_TYPES = {
    "serve_here": {"name": "В заведении (в чашке) ☕"},
    "serve_go": {"name": "На вынос (в стакане) 🥤"}
}

@bot.message_handler(commands=['start'])
def start_cafe(message):
    chat_id = message.chat.id
    if chat_id not in user_states:
        user_states[chat_id] = {
            'cart': [], 'current_item': None,
            'address': None, 'phone': None, 'stamps': 4
        }
    show_main_menu(chat_id)

def show_main_menu(chat_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    for key, val in MENU.items():
        markup.add(types.InlineKeyboardButton(f"{val['name']} — ${val['price']}", callback_data=f"buy_{key}"))
    if user_states[chat_id]['cart']:
        markup.add(types.InlineKeyboardButton(f"🛒 Перейти в корзину ({len(user_states[chat_id]['cart'])} экз.)", callback_data="go_cart"))
    
    stamps = user_states[chat_id]['stamps']
    stamps_view = "🔴" * stamps + "⚪" * (5 - stamps)
    bot.send_message(chat_id, f"☕ *Coffee Express Premium* приветствует вас!\n\nКаждый 6-й кофе у нас БЕСПЛАТНО! 🎁\nВаш баланс: {stamps_view} (Осталось {6 - stamps} чаш. до подарка)\n\n*Выберите напиток для добавления в корзину:*", parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_logic(call):
    chat_id = call.message.chat.id
    data = call.data
    if chat_id not in user_states: return

    # Шаг 1: Выбор напитка -> Спрашиваем формат (Чашка / Стакан)
    if data.startswith("buy_"):
        item_key = data.replace("buy_", "")
        user_states[chat_id]['current_item'] = {'key': item_key, 'size': 'size_m', 'syrup': None, 'serve': None}
        
        markup = types.InlineKeyboardMarkup(row_width=1)
        for key, val in SERVE_TYPES.items():
            markup.add(types.InlineKeyboardButton(val['name'], callback_data=f"setserve_{key}"))
        bot.edit_message_text(f"Вы выбрали: *{MENU[item_key]['name']}*.\n\n📍 Где будете пить кофе?", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # Шаг 2: Умное ветвление
    elif data.startswith("setserve_"):
        serve_key = data.replace("setserve_", "")
        user_states[chat_id]['current_item']['serve'] = serve_key
        current = user_states[chat_id]['current_item']
        
        if serve_key == "serve_here":
            user_states[chat_id]['current_item']['size'] = "size_m" # Посуда фиксированная
            markup = types.InlineKeyboardMarkup(row_width=2)
            btns = [types.InlineKeyboardButton(val['name'], callback_data=f"syrup_{key}") for key, val in SYRUPS.items()]
            markup.add(*btns)
            bot.edit_message_text(f"Вы выбрали: *{MENU[current['key']]['name']}*\n📍 Формат: {SERVE_TYPES[serve_key]['name']}\n\n✨ Желаете добавить топпинг/сироп?", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup(row_width=1)
            for key, val in SIZES.items():
                price_text = f" (🌐 Базовая)" if val['price'] == 0 else f" (+${val['price']:.2f})"
                markup.add(types.InlineKeyboardButton(f"{val['name']}{price_text}", callback_data=f"setsize_{key}"))
            bot.edit_message_text(f"Вы выбрали: *{MENU[current['key']]['name']}*\n📍 Формат: {SERVE_TYPES[serve_key]['name']}\n\n📐 Выберите размер бумажного стакана:", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # Шаг 3: Выбор размера (только на вынос)
    elif data.startswith("setsize_"):
        size_key = data.replace("setsize_", "")
        user_states[chat_id]['current_item']['size'] = size_key
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        btns = [types.InlineKeyboardButton(val['name'], callback_data=f"syrup_{key}") for key, val in SYRUPS.items()]
        markup.add(*btns)
        
        current = user_states[chat_id]['current_item']
        bot.edit_message_text(f"Вы выбрали: *{MENU[current['key']]['name']}*\n📍 Формат: {SERVE_TYPES[current['serve']]['name']}\n📐 Размер стакана: {SIZES[size_key]['name']}\n\n✨ Желаете добавить топпинг/сироп?", chat_id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    # Шаг 4: Выбор сиропа -> В корзину
    elif data.startswith("syrup_"):
        syrup_key = data.replace("syrup_", "")
        current = user_states[chat_id]['current_item']
        current['syrup'] = syrup_key
        
        user_states[chat_id]['cart'].append(current)
        user_states[chat_id]['current_item'] = None
        
        bot.delete_message(chat_id, call.message.message_id)
        bot.send_message(chat_id, f"✅ {MENU[current['key']]['name']} добавлен в корзину!")
        show_main_menu(chat_id)

    # Перенаправление во 2-ю часть файла
    elif data == "go_cart": render_cart(chat_id, call.message.message_id)
    elif data.startswith("del_"): handle_deletion(chat_id, data, call.message.message_id)
    elif data == "back_menu": bot.delete_message(chat_id, call.message.message_id); show_main_menu(chat_id)
    elif data == "order_start": start_order_checkout(chat_id, call.message.message_id)
# Функция отрисовки премиум-корзины
def render_cart(chat_id, message_id):
    cart = user_states[chat_id]['cart']
    stamps_before = user_states[chat_id]['stamps']
    
    total_items_price = 0.0
    cart_text = "🛒 *Ваша корзина:*\n\n"
    prices_list = []
    markup = types.InlineKeyboardMarkup()
    
    for idx, item in enumerate(cart):
        base = MENU[item['key']]
        size = SIZES[item['size']]
        syrup = SYRUPS[item['syrup']]
        serve = SERVE_TYPES[item['serve']]
        
        # Считаем цену позиции: база + размер + сироп
        item_price = base['price'] + size['price'] + syrup['price']
        total_items_price += item_price
        prices_list.append(base['price'] + size['price'])
        
        # Умное отображение размера (прячем для чашек)
        if item['serve'] == 'serve_go':
            size_line = f"   ├ Размер: {size['name']}\n"
        else:
            size_line = ""
            
        cart_text += (f"{idx + 1}. *{base['name']}*\n"
                      f"   ├ Формат: _{serve['name']}_\n"
                      f"{size_line}"
                      f"   ├ Топпинг: {syrup['name']}\n"
                      f"   💵 Цена: ${item_price:.2f}\n\n")
        
        markup.add(types.InlineKeyboardButton(f"❌ Удалить поз. {idx + 1}", callback_data=f"del_{idx}"))
    
    # Расчет скидки по программе лояльности
    total_stamps = stamps_before + len(cart)
    bonus_count = total_stamps // 6
    discount = 0.0
    
    if bonus_count > 0:
        prices_list.sort()
        for i in range(min(bonus_count, len(prices_list))):
            discount += prices_list[i]
            
    final_price = total_items_price - discount
    user_states[chat_id]['calculated_price'] = final_price
    user_states[chat_id]['discount'] = discount
    user_states[chat_id]['new_stamps'] = total_stamps % 6
    
    cart_text += f"▪️ Сумма позиций: ${total_items_price:.2f}\n"
    if discount > 0:
        cart_text += f"🎁 *Бонус (Каждый 6-й бесплатно): -${discount:.2f}*\n"
    cart_text += f"💰 *Итоговая сумма к оплате: ${final_price:.2f}*"
    
    markup.row(types.InlineKeyboardButton("➕ Добавить еще", callback_data="back_menu"),
               types.InlineKeyboardButton("🚀 Оформить заказ", callback_data="order_start"))
    
    bot.edit_message_text(cart_text, chat_id, message_id, parse_mode="Markdown", reply_markup=markup)

# Функция удаления товара
def handle_deletion(chat_id, data, message_id):
    idx_to_remove = int(data.replace("del_", ""))
    if 0 <= idx_to_remove < len(user_states[chat_id]['cart']):
        user_states[chat_id]['cart'].pop(idx_to_remove)
    
    if not user_states[chat_id]['cart']:
        bot.delete_message(chat_id, message_id)
        bot.send_message(chat_id, "🛒 Ваша корзина опустела.")
        show_main_menu(chat_id)
    else:
        render_cart(chat_id, message_id)

# Оформление заказа и умная проверка формата выдачи
def start_order_checkout(chat_id, message_id):
    cart = user_states[chat_id]['cart']
    
    # Анализируем состав корзины
    count_go = sum(1 for item in cart if item['serve'] == 'serve_go')
    count_here = sum(1 for item in cart if item['serve'] == 'serve_here')
    
    need_delivery = count_go > 0
    user_states[chat_id]['need_delivery'] = need_delivery
    
    bot.edit_message_text(f"🛒 *Ваша корзина:*\n\n💰 К оплате: *${user_states[chat_id]['calculated_price']:.2f}*\n\n↳ *Статус:* Начинаем оформление заказа... ⏳", chat_id, message_id, parse_mode="Markdown")
    
    if need_delivery:
        # Динамический текст подсказки в зависимости от состава товаров в заказе
        if count_here > 0:
            prompt_text = "📍 В вашем заказе есть позиции на вынос. Укажите адрес доставки или напишите 'В заведении', если заберете у стойки:"
        else:
            prompt_text = "📍 Вы взяли кофе на вынос. Укажите адрес доставки или напишите 'В заведении', если заберете у стойки:"
            
        msg = bot.send_message(chat_id, prompt_text)
        bot.register_next_step_handler(msg, get_address)
    else:
        user_states[chat_id]['address'] = "В заведении (Выдать за столик)"
        msg = bot.send_message(chat_id, "📞 Введите ваш номер телефона для подтверждения заказа:")
        bot.register_next_step_handler(msg, get_phone)

def get_address(message):
    chat_id = message.chat.id
    if message.text == '/start': start_cafe(message); return
    
    user_states[chat_id]['address'] = message.text
    msg = bot.send_message(chat_id, "📞 Введите ваш номер телефона для связи с вами:")
    bot.register_next_step_handler(msg, get_phone)

def get_phone(message):
    chat_id = message.chat.id
    if message.text == '/start': start_cafe(message); return
    
    user_states[chat_id]['phone'] = message.text
    state = user_states[chat_id]
    items_summary = []
    
    for item in state['cart']:
        size_name = f", {SIZES[item['size']]['name']}" if item['serve'] == 'serve_go' else ""
        items_summary.append(f"{MENU[item['key']]['name']} ({SERVE_TYPES[item['serve']]['name']}{size_name})")
    
    summary_text = "; ".join(items_summary)
    username = f"@{message.from_user.username}" if message.from_user.username else "Не указан"
    
    kitchen_message = (
        f"🛎️ *НОВЫЙ ЗАКАЗ В COFFEE EXPRESS!* 🛎️\n\n"
        f"👤 *Клиент:* {username}\n"
        f"📞 *Телефон:* {state['phone']}\n"
        f"📍 *Зона выдачи/Адрес:* {state['address']}\n\n"
        f"📦 *Детали заказа:* {summary_text}\n"
        f"🎁 *Скидка лояльности:* -${state['discount']:.2f}\n"
        f"💰 *Итоговый чек:* ${state['calculated_price']:.2f}\n"
        f"📊 *Новый баланс штампов:* {state['new_stamps']} чаш."
    )
    # Проверка режима работы кофейни (с 08:00 до 22:00)
    import datetime
    current_hour = datetime.datetime.now().hour

    # Формируем сообщение для администратора/бариста
    bot.send_message(YOUR_CHAT_ID, lead_message, parse_mode="Markdown")

    # Логика ответа клиенту в зависимости от времени
    if 8 <= current_hour < 22:
        # Рабочее время
        bot.send_message(chat_id, f"☕️ *Заказ успешно передан бариста!*\n\n• Итого к оплате: *${state['calculated_price']}*\n\nПриготовим за 10 минут! 🎉")
    else:
        # Ночное время
        bot.send_message(chat_id, f"🌙 *Наша кофейня сейчас закрыта* (работаем с 08:00 до 22:00).\n\nНо мы зафиксировали ваш заказ на сумму *${state['calculated_price']}* в системе! Администратор свяжется с вами сразу же утром, чтобы подтвердить удобное время выдачи. Спасибо! ☕️")

    del user_states[chat_id]


print("Финальный ультимативный бот кофейни запущен!")
# Автоматическая настройка синего меню команд для кофейни
bot.set_my_commands([
    types.BotCommand("start", "☕️ Перезапустить меню кофейни"),
    types.BotCommand("help", "📞 Связь с администратором студии")
])

bot.infinity_polling()