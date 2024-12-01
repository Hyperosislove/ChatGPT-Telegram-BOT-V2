import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, ApplicationBuilder, ContextTypes

import openai

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Ensure tokens are available
if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("TELEGRAM_BOT_TOKEN and OPENAI_API_KEY must be set in Heroku config vars.")

# Set OpenAI API key
openai.api_key = OPENAI_API_KEY

# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalam-o-Alaikum! Main aapka AI assistant hoon. Kuch puchhna ho to message karein.")

# Handle text messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("Maaf kijiye, main abhi aapki request process nahi kar sakta.")

# Main function to start the bot
def main():
    # Initialize the bot application
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # Add command and message handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start polling
    application.run_polling()

if __name__ == "__main__":
    main()
