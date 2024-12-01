import os
import time
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_BOT_TOKEN or not OPENAI_API_KEY:
    raise ValueError("TELEGRAM_BOT_TOKEN and OPENAI_API_KEY must be set as environment variables.")

openai.api_key = OPENAI_API_KEY

# Start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalam-o-Alaikum! Main aapka AI assistant hoon. Kuch puchhna ho to message karein.")

# Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    try:
        # Generate response from OpenAI
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=user_message,
            max_tokens=150,
            temperature=0.7
        )
        reply = response.choices[0].text.strip()
        await update.message.reply_text(reply)
        time.sleep(1)  # Add delay to prevent flooding
    except openai.error.AuthenticationError:
        await update.message.reply_text("Error: Invalid OpenAI API Key.")
    except openai.error.RateLimitError:
        await update.message.reply_text("Error: Rate limit exceeded. Please try later.")
    except Exception as e:
        await update.message.reply_text(f"Unexpected Error: {str(e)}")

# Main Application
def main():
    application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.run_polling()

if __name__ == "__main__":
    main()
