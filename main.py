# import emoji
# print(emoji.emojize('Python is :thumbs_up:'))

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from bot_commands import *



app = ApplicationBuilder().token("6070398445:AAHhYaCpDSS1tyQubNKSztSUFxnnPz0IeKo").build()

app.add_handler(CommandHandler("start", hi_commands))
app.add_handler(CommandHandler("time", time_commands))
app.add_handler(CommandHandler("help", help_commands))
app.add_handler(CommandHandler("sum", sum_commands))
app.add_handler(CommandHandler("NY", days_to_NY_command))
app.add_handler(CommandHandler("AURORA", getaurora))
app.add_handler(CommandHandler("GAME", gamestart))
app.add_handler(CallbackQueryHandler(callback_commands))

app.add_handler(MessageHandler(None, message_processing))
  # создаем игру

print("server start")
app.run_polling()