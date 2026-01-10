import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters
from brain import process_message

# 1. Load the token FIRST
load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # This function is for responding to /start
    await update.message.reply_text("Welcome! I am back online and ready to help with Python!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    bot_response = process_message(user_text)
    await update.message.reply_text(bot_response)

if __name__ == '__main__':
    if not TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found in .env file")
    else:
        # 2. Build the app using the new token
        app = ApplicationBuilder().token(TOKEN).job_queue(None).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

        print("🤖 Telegram bot is running with the NEW token...")
        app.run_polling()