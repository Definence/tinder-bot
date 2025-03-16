from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

import pdb
from gpt import *
from util import *

# https://t.me/tinder_bolt_helper_bot
TOKEN = "7746282763:AAHMsKOVgnYck9LxNkHqK-08LfVYby8rahI"

async def start(update, context):
  msg = load_message("main")
  await send_text(update, context, msg)

async def hello(update, context):
  await send_text_buttons(update, context, "Hello" + update.message.text, {
    "start": 'START',
    'stop': 'STOP',
  })

async def buttons_handler(update, context):
  query = update.callback_query.data
  # pdb.set_trace()
  if query == "start":
    await send_text(update, context, "Started")
  elif query == "stop":
    await send_text(update, context, "Stopped")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, hello))
app.add_handler(CallbackQueryHandler(buttons_handler))

app.run_polling()
