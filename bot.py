from idlelib import query

from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

import pdb
from gpt import *
from util import *

# https://t.me/tinder_bolt_helper_bot
TELEGRAM_TOKEN = '7746282763:AAHMsKOVgnYck9LxNkHqK-08LfVYby8rahI'
OPEN_AI_TOKEN = 'gpt:AU54YW8RRi4TXANWp060hfjiJxU6btLIvPmqxAgYF0QLgPDwmNfdLT5NyC9Y8r_u4QZeQmwhzFJFkblB3T4yhgCdA9W2KZIQwDchnwN-SRJKHph3pqraKQNsAmcDeSXdm_4aNY-8_3oiLFalGXckzNJlfA-T'

# main
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

async def message(update, context):
  dialog.mode = 'message'
  msg = load_message('message')
  await send_photo(update, context, 'message')
  await send_text_buttons(update, context, msg, {
    'message_next': 'Написати повідомлення',
    'message_date': 'Запросити на побачення '
  })
  dialog.list.clear()


# handlers
async def send_text_handler(update, context):
  if dialog.mode == 'gpt':
    await gpt_dialog(update, context)
  elif dialog.mode == 'date':
    await date_dialog(update, context)
  elif dialog.mode == 'message':
    await message_dialog(update, context)
  else:
    await send_text(update, context, 'Hello ' + update.message.text)

async def date_button_handler(update, context):
  dialog.mode = 'date' # just in case triggered in other mode
  query = update.callback_query.data
  await update.callback_query.answer()
  await send_photo(update, context, query)
  await send_text(update, context, 'Гарний вибір.\uD83D\uDE05 Ваша задача запросити дівчину / хлопця за пʼять повідомлень\uFE0F')
  chatgpt.set_prompt(load_prompt(query))

async def message_button_handler(update, context):
  q = update.callback_query.data
  dialog.mode = 'message'
  await update.callback_query.answer()
  prompt = load_prompt(q)
  user_chat_history = "\n\n".join(dialog.list)
  my_message = await send_text(update, context, 'Думаю над варіантами...')
  answer = await chatgpt.send_question(prompt, user_chat_history)
  await my_message.edit_text(answer)

# gpt dialogs
async def gpt_dialog(update, context):
  text = update.message.text
  prompt = load_prompt('gpt')
  answer = await chatgpt.send_question(prompt, text)
  await send_text(update, context, answer)

async def date_dialog(update, context):
  # pdb.set_trace()
  text = update.message.text
  typing_msg  = await send_text(update, context, 'Набирає повідомлення...')
  answer = await chatgpt.add_message(text)
  await typing_msg.edit_text(answer)

async def message_dialog(update, context):
  text = update.message.text
  dialog.list.append(text)

dialog = Dialog()
dialog.mode = None
dialog.list = []

chatgpt = ChatGptService(token=OPEN_AI_TOKEN)

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler('start', start))
app.add_handler(CommandHandler('gpt', gpt))
app.add_handler(CommandHandler('date', date))
app.add_handler(CommandHandler('message', message))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_text_handler))
app.add_handler(CallbackQueryHandler(date_button_handler, pattern='^date_.*'))
app.add_handler(CallbackQueryHandler(message_button_handler, pattern='^message_.*'))
app.run_polling()
