from telebot import TeleBot, types
import telebot
from flask import Flask, request
import os

bot = TeleBot("7959291954:AAFrKLqU3J9FmVo1sTHuz_9hl58XqGqCGWI")  
server = Flask(__name__)

required_channel = ("@shokh_movie", "@World_Movie_Uzb")

films = {
    "1": "https://t.me/shokh_movie/21",
    "2": "https://t.me/shokh_movie/22",
    "3": "https://t.me/shokh_movie/23",
    "4": "https://t.me/shokh_movie/26",
    "5": "https://t.me/shokh_movie/28",
    "6": "https://t.me/shokh_movie/29",
    "7": "https://t.me/shokh_movie/30",
    "8": "https://t.me/shokh_movie/31",
    "9": "https://t.me/shokh_movie/32",
    "10": "https://t.me/shokh_movie/33",
    "11": "https://t.me/shokh_movie/34",
    "12": "https://t.me/shokh_movie/37",
    "13": "https://t.me/shokh_movie/38",
    "14": "https://t.me/shokh_movie/39",
    "15": "https://t.me/shokh_movie/40",
    "16": "https://t.me/shokh_movie/41",
    "17": "https://t.me/shokh_movie/42",
    "18": "https://t.me/shokh_movie/44",
    "19": "https://t.me/shokh_movie/45",
    "20": "https://t.me/shokh_movie/46",
    "21": "https://t.me/shokh_movie/47",
    "22": "https://t.me/shokh_movie/48",
    "23": "https://t.me/shokh_movie/49",
    "24": "https://t.me/shokh_movie/50",
    "25": "https://t.me/shokh_movie/60",
    "27": "https://t.me/shokh_movie/58",
}

def check_subscription(user_id):
    try:
        for channel in required_channel:
            member = bot.get_chat_member(channel, user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        return True
    except Exception:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if not check_subscription(message.from_user.id):
        markup = types.InlineKeyboardMarkup()
        kanal1 = types.InlineKeyboardButton("📢 Shokh_movie", url="https://t.me/shokh_movie")
        kanal2 = types.InlineKeyboardButton("🎬 World_Movie_Uz", url="https://t.me/World_Movie_Uzb")
        check_btn = types.InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")
        
        markup.add(kanal1)
        markup.add(kanal2)
        markup.add(check_btn)

        bot.send_message(
            message.chat.id,
            "❗ Botdan foydalanish uchun avval kanalimizga a’zo bo‘ling!",
            reply_markup=markup
        )
    else:
        send_welcome(message)

@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def check_sub(call):
    if check_subscription(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Obuna tasdiqlandi!")
        send_welcome(call.message)
    else:
        bot.answer_callback_query(call.id, "❗ Hali kanalga a’zo bo‘lmadingiz!")

def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    kanal_btn = types.InlineKeyboardButton("📢 Telegram Kanal", url="https://t.me/shokh_movie")
    insta_btn = types.InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/shokh_movie")
    markup.add(kanal_btn, insta_btn)

    text = (
        "Assalomu alaykum! 🎬\n"
        "Botimizga xush kelibsiz!\n\n"
        "👉 Qidirayotgan kino kodini yozib yuboring.\n"
        "Masalan: 1, 2, 3"
    )

    bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def search(message):
    if not check_subscription(message.from_user.id):
        start(message)
        return

    query = message.text.strip()
    if query in films:
        bot.send_message(message.chat.id, f"🎬 Mana siz izlagan kino:\n{films[query]}")
    else:
        bot.send_message(message.chat.id, "😔 Bunday kod topilmadi. Iltimos, boshqa kod yozib ko‘ring.")

# --- Flask routes ---
@server.route("/" + bot.token, methods=['POST'])
def getMessage(): 
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/", methods=['GET'])
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://shokh-movie-bot-1.onrender.com/" + bot.token)
    return "Webhook set", 200

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    server.run(host="0.0.0.0", port=port)
