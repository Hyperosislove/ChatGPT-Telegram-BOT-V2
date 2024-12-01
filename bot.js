const { Telegraf } = require('telegraf');
const { Configuration, OpenAIApi } = require('openai');

// Set up Telegraf Bot
const bot = new Telegraf(process.env.TELEGRAM_BOT_TOKEN);

// Set up OpenAI API client
const openai = new OpenAIApi(new Configuration({
  apiKey: process.env.OPENAI_API_KEY,
}));

// Start command
bot.start((ctx) => ctx.reply('Hello! I am an AI-powered bot. Ask me anything!'));

// Handle messages
bot.on('text', async (ctx) => {
  const userMessage = ctx.message.text;
  
  const openaiResponse = await openai.createCompletion({
    model: 'text-davinci-003',
    prompt: userMessage,
    max_tokens: 150,
  });
  
  const aiResponse = openaiResponse.data.choices[0].text.trim();
  ctx.reply(aiResponse);
});

// Start bot
bot.launch();
