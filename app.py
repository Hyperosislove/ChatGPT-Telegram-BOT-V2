from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
import openai
import os

# Flask app initialization
app = Flask(__name__)

# Load API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ChatGPT session storage (to maintain context per user)
user_sessions = {}

def handle_message(update, context):
    """Handles incoming messages from Telegram."""
    chat_id = update.message.chat_id
    user_message = update.message.text

    # Initialize user session if not exists
    if chat_id not in user_sessions:
        user_sessions[chat_id] = []

    # Append user message to session
    user_sessions[chat_id].append({"role": "user", "content": user_message})

    # Call OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=user_sessions[chat_id]
    )

    # Get the reply
    bot_reply = response['choices'][0]['message']['content']

    # Append bot reply to session
    user_sessions[chat_id].append({"role": "assistant", "content": bot_reply})

    # Send reply to user
    bot.send_message(chat_id=chat_id, text=bot_reply)

@app.route(f"/{TELEGRAM_BOT_TOKEN}", methods=["POST"])
def webhook():
    """Handles webhook requests from Telegram."""
    update = Update.de_json(request.get_json(force=True), bot)
    dispatcher.process_update(update)
    return "OK", 200

# Setup Telegram dispatcher
dispatcher = Dispatcher(bot, None)
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
