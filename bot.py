from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

import pdb
from gpt import *
from util import *

# https://t.me/tinder_bolt_helper_bot
TELEGRAM_TOKEN = '7746282763:AAHMsKOVgnYck9LxNkHqK-08LfVYby8rahI'
OPEN_AI_TOKEN = 'gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T'

async def start(update, context):
  await send_photo(update, context, 'main')
  await send_text(update, context, load_message('main'))
  await show_main_menu(update, context, {
    'start': 'Головне меню',
    'profile': 'Генерація Tinder-профіля \U0001F3D0',
    'opener': 'Повідомлення для знайомства \U0001F3B0',
    'message': 'Переписка від вашого імені \U0001F3D8',
    'date': 'Спілкування з зірками \U0001F4A5',
    'gpt': 'Задати питання ChatGPT \U0001F3B0'
  })

async def gpt(update, context):
  dialog.mode = 'gpt'
  await send_photo(update, context, 'gpt')
  await send_text(update, context, load_message('gpt'))

async def send_text_handler(update, context):
  if dialog.mode == 'gpt':
    await gpt_dialog(update, context)
  elif dialog.mode == 'date':
    await date_dialog(update, context)
  else:
    await send_text(update, context, 'Hello ' + update.message.text)

async def gpt_dialog(update, context):
  text = update.message.text
  prompt = load_prompt('gpt')
  answer = await chatgpt.send_question(prompt, text)
  await send_text(update, context, answer)

async def date(update, context):
  dialog.mode = 'date'
  await send_photo(update, context, 'date')
  await send_text_buttons(update, context, load_message('date'), {
    'date_grande': 'Аріана Гранде',
    'date_robbie': 'Марго Роббі',
    'date_zendaya': 'Зендея',
    'date_gosling': 'Райан Гослінг',
    'date_hardy': 'Том Харді',
  })

async def date_button(update, context):
  dialog.mode = 'date' # just in case triggered in other mode
  query = update.callback_query.data
  await update.callback_query.answer()
  await send_photo(update, context, query)
  await send_text(update, context, 'Гарний вибір.\uD83D\uDE05 Ваша задача запросити дівчину / хлопця за пʼять повідомлень\uFE0F')
  chatgpt.set_prompt(load_prompt(query))

async def date_dialog(update, context):
  # pdb.set_trace()
  text = update.message.text
  typing_msg  = await send_text(update, context, 'Набирає повідомлення...')
  answer = await chatgpt.add_message(text)
  await typing_msg.edit_text(answer)


dialog = Dialog()
dialog.mode = None
chatgpt = ChatGptService(token=OPEN_AI_TOKEN)
app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('date', date))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_text_handler))
app.add_handler(CallbackQueryHandler(date_button, pattern='^date_.*'))
app.run_polling()
