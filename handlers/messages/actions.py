from aiogram import types
from keyboards.inline import new_keyboard_income_expense, vote_cb2
from keyboards.inline import vote_cb, get_expense_type_keyboard
from loader import dp
from storage.postgres import add_income, add_outcome


@dp.message_handler()
async def send_action_keyboard(message: types.Message):
    if message.text.isdigit():
        await message.reply("Выберите действия:", reply_markup=new_keyboard_income_expense(message.text))
    else:
        pass


@dp.callback_query_handler(vote_cb.filter(action='income'))
async def get_income(query: types.CallbackQuery, callback_data: dict):
    add_income(callback_data['amount'], query.message.chat.id, query.from_user.full_name)
    await query.message.edit_text('Добавлено в Доход 📈')


@dp.callback_query_handler(vote_cb.filter(action='expense type'))
async def send_expense_type_keyboard(query: types.CallbackQuery, callback_data: dict):
    await query.message.edit_text('Выберите тип расходов', reply_markup=get_expense_type_keyboard(query.message.chat.id,
                                                                                                  callback_data[
                                                                                                      'amount']))


@dp.callback_query_handler(vote_cb2.filter(action='expense'))
async def get_expense(query: types.CallbackQuery, callback_data: dict):
    add_outcome(query.message.chat.id, callback_data['category_id'], callback_data['amount'])
    await query.message.edit_text(f'Потрачено на {callback_data["category"]}')
