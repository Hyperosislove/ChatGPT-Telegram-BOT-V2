import logging
import time
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import openai
from config import bot_token, api_key
from message_templates import message_templates

logging.basicConfig(level=logging.INFO)

bot = Bot(token=bot_token)
dp = Dispatcher(bot)

openai.api_key = api_key

messages = {}
user_languages = {}  # Track the user's language preference

@dp.callback_query_handler(lambda c: c.data in ['en', 'ru', 'ua'])
async def process_language_selection(callback_query: types.CallbackQuery):
    user_languages[callback_query.from_user.id] = callback_query.data
    await send_message(callback_query.from_user.id, 'language_confirmation')
    await bot.answer_callback_query(callback_query.id)

# Language selection keyboard
language_keyboard = InlineKeyboardMarkup(row_width=2)
language_keyboard.add(
    InlineKeyboardButton("English🇬🇧", callback_data='en'),
    InlineKeyboardButton("Русский🇷🇺", callback_data='ru'),
    InlineKeyboardButton("Український🇺🇦", callback_data='ua')
)

async def send_message(user_id, message_key):
    language = user_languages.get(user_id, 'en')  # Default to English if no language selected
    message_template = message_templates[language][message_key]
    await bot.send_message(user_id, message_template)

@dp.message_handler(commands=['language'])
async def language_cmd(message: types.Message):
    await bot.send_message(message.chat.id, message_templates['en']['language_selection'],
                           reply_markup=language_keyboard)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    try:
        user_id = message.from_user.id
        if user_id not in messages:
            messages[user_id] = []
        language = user_languages.get(user_id, 'en')  # Default to English
        await message.reply(message_templates[language]['start'])
    except Exception as e:
        logging.error(f'Error in start_cmd: {e}')

@dp.message_handler(commands=['newtopic'])
async def new_topic_cmd(message: types.Message):
    try:
        user_id = message.from_user.id
        messages[user_id] = []
        language = user_languages.get(user_id, 'en')
        await message.reply(message_templates[language]['newtopic'])
    except Exception as e:
        logging.error(f'Error in new_topic_cmd: {e}')

@dp.message_handler(commands=['image'])
async def send_image(message: types.Message):
    try:
        description = message.text.replace('/image', '').strip()
        language = user_languages.get(message.from_user.id, 'en')
        if not description:
            await message.reply(message_templates[language]['image_prompt'])
            return
        image_url = await generate_image(description)
        await bot.send_photo(chat_id=message.chat.id, photo=image_url)
    except Exception as e:
        language = user_languages.get(message.from_user.id, 'en')
        await message.reply(message_templates[language]['image_error'] + str(e))

async def generate_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="512x512",
        response_format="url",
    )
    return response['data'][0]['url']

@dp.message_handler(commands=['help'])
async def help_cmd(message: types.Message):
    language = user_languages.get(message.from_user.id, 'en')
    await message.reply(message_templates[language]['help'])

@dp.message_handler(commands=['about'])
async def about_cmd(message: types.Message):
    language = user_languages.get(message.from_user.id, 'en')
    await message.reply(message_templates[language]['about'])

@dp.message_handler()
async def echo_msg(message: types.Message):
    try:
        user_message = message.text
        user_id = message.from_user.id

        if user_id not in messages:
            messages[user_id] = []
        messages[user_id].append({"role": "user", "content": user_message})

        # OpenAI conversation handling
        language = user_languages.get(user_id, 'en')
        processing_message = await message.reply(message_templates[language]['processing'])

        await bot.send_chat_action(chat_id=message.chat.id, action="typing")

        completion = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=messages[user_id],
            max_tokens=2500,
            temperature=0.7,
            frequency_penalty=0,
            presence_penalty=0,
            user=user_id
        )
        chatgpt_response = completion.choices[0]['message']

        messages[user_id].append({"role": "assistant", "content": chatgpt_response['content']})
        await message.reply(chatgpt_response['content'])
        await bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)
    except Exception as ex:
        logging.error(f'Error in echo_msg: {ex}')
        await message.reply("An error occurred. Please try again later.")
        await new_topic_cmd(message)

if __name__ == '__main__':
    executor.start_polling(dp)
