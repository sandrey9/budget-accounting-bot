from aiogram import types
from storage.postgres import select_outcome_category
from aiogram.utils.callback_data import CallbackData

vote_cb = CallbackData('vote', 'action', 'amount')
vote_cb2 = CallbackData('vote', 'action', 'category', 'category_id', 'amount')


def new_keyboard_income_expense(amount):
    return types.InlineKeyboardMarkup().row(
        types.InlineKeyboardButton('📈Доход', callback_data=vote_cb.new(action='income', amount=amount)),
        types.InlineKeyboardButton('📉Расход', callback_data=vote_cb.new(action='expense type', amount=amount)))


def get_expense_type_keyboard(chat_id, amount):
    keyboard = types.InlineKeyboardMarkup().row()
    for category, category_id in select_outcome_category(chat_id):
        keyboard.insert(types.InlineKeyboardButton(category,
                                                   callback_data=vote_cb2.new(action='expense', category=category,
                                                                              category_id=category_id, amount=amount)))
    return keyboard


def get_expense_type_keyboard_to_delete(chat_id):
    keyboard = types.InlineKeyboardMarkup().row()
    for text, c_id in select_outcome_category(chat_id):
        keyboard.insert({"text": text, "callback_data": f"delete_et:{c_id}"})
    keyboard.insert({"text": 'Отмена', "callback_data": "cancel"})
    return keyboard

# {"inline_keyboard": [[{"text": "📈Доход", "callback_data": "vote:income:222"},
# {"text": "📉Расход", "callback_data": "vote:expense:222"}]]}
# x.insert(types.InlineKeyboardButton('📉Расход', callback_data=vote_cb.new(action='expense', amount=amount)))
