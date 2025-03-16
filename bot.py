from telegram.ext import ApplicationBuilder, MessageHandler, filters, CallbackQueryHandler, CommandHandler

from gpt import *
from util import *

# тут будемо писати наш код :)


app = ApplicationBuilder().token("telegram-token").build()
app.run_polling()
