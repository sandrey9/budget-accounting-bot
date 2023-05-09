import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token=os.getenv('BOT_TOKEN'), parse_mode=types.ParseMode.HTML)
# Тут погружаем все переменные которые нужны для хендлеров

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.ERROR, filename='budget.log', filemode='a',
                    format='%(asctime)s ; %(message)s ; %(levelname)s ; %(filename)s:%(lineno)s')
logger.setLevel(logging.DEBUG)
