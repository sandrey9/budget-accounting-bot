from aiogram import types
from storage.postgres import select_outcome_category
from aiogram.utils.callback_data import CallbackData

budgets_query = CallbackData('budget', 'action', 'amount')
categories_query = CallbackData('category', 'action', 'category_name', 'category_id', 'amount')


def create_income_outcome_keyboard(amount):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('📈Доход', callback_data=budgets_query.new(action='add income', amount=amount)),
        types.InlineKeyboardButton('📉Расход', callback_data=budgets_query.new(action='send category', amount=amount)))


def create_outcome_category_keyboard(chat_id, action, amount=0):
    keyboard = types.InlineKeyboardMarkup().row()
    for category_name, category_id in select_outcome_category(chat_id):
        keyboard.insert(types.InlineKeyboardButton(category_name,
                                                   callback_data=categories_query.new(action=action,
                                                                                      category_name=category_name,
                                                                                      category_id=category_id,
                                                                                      amount=amount)))
    keyboard.insert({"text": 'Отмена', "callback_data": "cancel"})
    return keyboard
