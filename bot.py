import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Load environment variables (Heroku Config Vars)
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure tokens are available
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("TELEGRAM_BOT_TOKEN and OPENAI_API_KEY must be set in Heroku config vars.")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Start command
def start(update, context):
    update.message.reply_text("Assalam-o-Alaikum! Main aapka AI assistant hoon. Kuch puchhna ho to message karein.")

# Handle text messages
def handle_message(update, context):
    user_message = update.message.text

    try:
        # Generate a response using OpenAI API
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_message,
            max_tokens=150,
            temperature=0.7
        )
        reply = response.choices[0].text.strip()
        update.message.reply_text(reply)
    except Exception as e:
        update.message.reply_text("Maaf kijiye, main abhi aapki request process nahi kar sakta.")

# Main function to start the bot
def main():
    # Initialize the Updater with Telegram Bot Token
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Command handler for /start
    dp.add_handler(CommandHandler("start", start))

    # Message handler for text messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
