from aiogram import types
from loader import dp


@dp.message_handler(commands=['start', 'help'])
async def process_start_command(message: types.Message):
    await message.reply('Тут описание слэш команд')
