from telegram import Update, InlineKeyboardButton, KeyboardButton
from telegram.ext import CommandHandler, ContextTypes, CallbackQueryHandler, InlineQueryHandler
import datetime
from spy import *
from play import *
from keyboards import *
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler
from time import sleep
from game import *
from random import randint
from datetime import datetime
import requests
game = Game()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)


async def start(update: Update, context: InlineKeyboardButton):
    keyboard = [
        [
            InlineKeyboardButton("option1", callback_data="1"),
            InlineKeyboardButton("option2", callback_data="2"),
        ],
        InlineKeyboardButton("option3", callback_data="3"),
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Пожалуйста выберите:", reply_markup=reply_markup)


async def hi_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, context)
    await update.message.reply_text(f'Привет! 👋, {update.effective_user.first_name}')
    botcommand = ['/NY - сколько осталось до нового года',
                  '/time - точное время',
                  '/sum - сумма двух чисел',
                  '/GAME - игра 50 спичек',
                  '/AURORA - прогноз полярных сияний']
    await update.message.reply_text('Команды бота:\n{}'.format('\n'.join(botcommand)))

def get_aurora():
    """прогноз полярных сияний
    https://services.swpc.noaa.gov/"""
    try:
        p = requests.get("https://services.swpc.noaa.gov/images/aurora-forecast-northern-hemisphere.jpg")
        out = open("aurora.jpg", "wb")
        out.write(p.content)
        out.close()
    except:
        return(None)
    return("aurora.jpg")

async def help_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, context)
    await update.message.reply_text(f'/hello\n/time\n/sum\n/rule - конфеты\n/xo - крестики нолики\n')


async def play_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, context)
    await update.message.reply_text(f'')


async def days_to_NY_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    now = datetime.today()
    NY = datetime(2024, 1, 1)
    d = NY-now
    await update.message.reply_text(f'До нового года осталось дней: {d.days}.')


async def time_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    log(update, context)
    await update.message.reply_text(f'{datetime.now().time()}')


async def sum_commands(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mess = update.message.text
    items = mess.split()
    a = int(items[1])
    b = int(items[2])
    await update.message.reply_text(a+b)


async def callback_commands(update: Update, callback: CallbackQueryHandler) -> None:
    if callback.data == "like":
        await callback.answer("Вам понравилось")


async def message_processing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка сырого текста в чате"""
    if update.message.text[0] != '/':
        if game.gamestatus:
            # запущена игра
            # ход игрока
            try:
                matches = int(update.message.text)
            except:
                await update.message.reply_text('Я не понял ваш ответ. Напишите цифрой, сколько вы берете спичек.')
                return
            if not 0 < matches < 9:
                await update.message.reply_text('можно брать только от 1 до 8 спичек')
                return
            game.action_player(matches)
            if game.check_game_state():
                await update.message.reply_text('Поздравляю вас, вы выиграли')
                game.stop()
                return
            message = f'На столе {game.heap} спичек.'
            await update.message.reply_text(message)
            sleep(1)
            # ход компьютера
            message = f'Я взял {game.action_cpu()} спичек\n'
            await update.message.reply_text(message)
            message = f'На столе {game.heap} спичек.'
            await update.message.reply_text(message)
            sleep(1)
            if game.check_game_state():
                message = f'Я выиграл'
                await update.message.reply_text(message)
                game.stop()
                return
            message = 'Ваш ход'
            await update.message.reply_text(message)
            return


async def gamestart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """старт игры"""
    if not game.gamestatus:
        game.start()
        message = game.help
        await update.message.reply_text(message)
        message = f'Игра началась.\nНа столе {game.heap} спичек\n'
        if randint(1, 100) > 50:
            message = 'Я хожу первый\n'
            message += f'Я взял {game.action_cpu()}\n'
            message += f'Осталось {game.heap}\nВаш ход'
            await update.message.reply_text(message)
        else:
            message = 'Ваш ход'
            await update.message.reply_text(message)


async def getaurora(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    aurora = get_aurora()
    if aurora == None:
        await update.message.reply_text('Данные не получены')
        return
    await update.message.reply_photo(aurora)


async def xo_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    mess = update.message.text.split()

    await update.message.reply_text(showMatrix())
    await update.message.reply_text(int(mess[1]))
    await update.message.reply_text(player(int(mess[1])))
    await update.message.reply_text(showMatrix())
