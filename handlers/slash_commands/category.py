from aiogram import types
from keyboards.inline import get_expense_type_keyboard_to_delete
from loader import dp
from storage.postgres import add_outcome_category, delete_outcome_category


@dp.message_handler(commands='category_add')
async def add_category(message: types.Message):
    if category_name := message.get_args():
        add_outcome_category(category_name, message.chat.id)
        await message.reply(f"Добавлена категория:{category_name}")
    else:
        await message.reply("Необходимо ввести название категории")


@dp.message_handler(commands='category_delete')
async def delete_category(message: types.Message):
    await message.reply("Какую категорию удалить:",
                        reply_markup=(get_expense_type_keyboard_to_delete(message.chat.id)))


@dp.callback_query_handler(text_contains='delete_et')
async def get_expense(call: types.CallbackQuery):
    _, btn_id = call.data.split(':')
    if len(delete_outcome_category(btn_id)) != 0:
        await call.message.edit_text('Удалено')
    else:
        await call.message.edit_text('Нельзя удалить')


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: types.CallbackQuery):
    await call.message.edit_text('Отменено')
