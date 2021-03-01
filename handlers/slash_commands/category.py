from aiogram import types

from keyboards.inline import create_outcome_categories_keyboard, categories_query
from loader import dp
from storage.postgres import add_outcome_category, delete_outcome_category


@dp.message_handler(commands="category_add")
async def add_category(message: types.Message):
    if category_name := message.get_args():
        add_outcome_category(category_name, message.chat.id)
        await message.reply(f"Добавлена категория:{category_name}")
    else:
        await message.reply("Необходимо ввести название категории")


@dp.message_handler(commands="category_delete")
async def select_category_to_delete(message: types.Message):
    await message.reply("Какую категорию удалить:",
                        reply_markup=create_outcome_categories_keyboard(message.chat.id, "delete category"))


@dp.callback_query_handler(categories_query.filter(action="delete category"))
async def delete_category(query: types.CallbackQuery, callback_data: dict):
    if delete_outcome_category(callback_data["category_id"]):
        await query.message.edit_text("Удалено")
    else:
        await query.message.edit_text("Нельзя удалить")


@dp.callback_query_handler(text="cancel")
async def cancel_buying(call: types.CallbackQuery):
    await call.message.edit_text("Отменено")
