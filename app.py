import os
import logging
import telebot
from flask import Flask, request, jsonify
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BOT_TOKEN = os.getenv("BOT_TOKEN")
PORT = int(os.getenv("PORT", 10000))  # Render uses port 10000
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL") + "/telegram"

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize bot and app
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Bot handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🎉 Bot is now LIVE! Use /help for commands.")

@bot.message_handler(commands=['help'])
def help(message):
    help_text = """
    🤖 Available Commands:
    /start - Start the bot
    /help - Show this help message
    /wallet - Check your balance
    /bet - Place a bet
    /pay - Add coins
    """
    bot.reply_to(message, help_text)

# Webhook endpoint
@app.route('/telegram', methods=['POST'])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_str = request.get_data(as_text=True)
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return jsonify({"status": "ok"})
    return jsonify({"error": "Invalid request"}), 400

# Health check endpoint
@app.route('/', methods=['GET'])
def health_check():
    return jsonify({"status": "Bot is running!"})

# Set webhook on startup
def set_webhook():
    try:
        bot.set_webhook(url=WEBHOOK_URL)
        logger.info(f"✅ Webhook set to: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"❌ Webhook setup failed: {e}")

if __name__ == '__main__':
    set_webhook()
    app.run(host='0.0.0.0', port=PORT)
