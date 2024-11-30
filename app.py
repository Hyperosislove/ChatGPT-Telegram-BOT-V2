from flask import Flask, request
from telegram import Bot, Update
from telegram.ext import Dispatcher, MessageHandler, Filters
import openai
import os

app = Flask(__name__)

# Load API keys from environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

# Initialize Telegram Bot
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Route to handle Telegram updates
@app.route(f'/{TELEGRAM_BOT_TOKEN}', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    dispatcher = Dispatcher(bot, None, workers=0)
    
    # Define the message handler
    def handle_message(update, context):
        user_message = update.message.text
        
        # Send the message to OpenAI for a response
        response = openai.Completion.create(
            model="text-davinci-003",  # You can change the model if needed
            prompt=user_message,
            max_tokens=150
        )
        
        # Send OpenAI response back to the user
        update.message.reply_text(response.choices[0].text.strip())
    
    # Add message handler
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Process the update
    dispatcher.process_update(update)
    
    return 'ok'

if __name__ == '__main__':
    app.run(debug=True)
