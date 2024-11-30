# ChatGPT Telegram Bot

An advanced ChatGPT-based Telegram bot that uses OpenAI's GPT-3.5 API for real-time messaging.

## Features
- Persistent chat history
- Multi-language support
- Custom commands like `/reset`, `/start`, and `/help`
- Rate limiting to avoid spam

## Deployment on Heroku
1. Fork this repository.
2. Go to [Heroku Dashboard](https://dashboard.heroku.com/) and create a new app.
3. Under "Deploy", connect your GitHub repository.
4. Add the following environment variables under "Settings" > "Config Vars":
   - `TELEGRAM_BOT_TOKEN`
   - `OPENAI_API_KEY`
5. Deploy the branch.
6. Set the bot's webhook URL:
