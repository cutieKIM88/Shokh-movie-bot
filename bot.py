import os
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")   # BotFather’dan olingan token
OMDB_API_KEY = os.getenv("OMDB_KEY")      # OMDb’dan olingan API key

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom 👋 Menga kino nomini yozing, men ma’lumot topib beraman 🎬")

async def search_movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    url = f"http://www.omdbapi.com/?t={query}&apikey={OMDB_API_KEY}"
    response = requests.get(url).json()

    if response.get("Response") == "True":
        title = response.get("Title")
        year = response.get("Year")
        plot = response.get("Plot")
        poster = response.get("Poster")

        msg = f"🎬 *{title}* ({year})\n\n{plot}"
        await update.message.reply_text(msg, parse_mode="Markdown")

        if poster and poster != "N/A":
            await update.message.reply_photo(poster)
    else:
        await update.message.reply_text("Kechirasiz, kino topilmadi 😔")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, search_movie))
    app.run_polling()

if __name__ == "__main__":
    main()
