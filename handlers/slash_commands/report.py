from aiogram import types
from loader import dp
import calendar
from storage.postgres import get_report_json
from aiogram.utils.markdown import hbold, hunderline


@dp.message_handler(state='*', commands=['report'])
async def send_report(message: types.Message):
    stats = message.get_args()
    if stats:
        year, month = stats.split('-')
        last_day = calendar.monthrange(int(year), int(month))[-1]
        start = f"{year}-{month}-01 00:00:00"
        end = f"{year}-{month}-{last_day} 23:59:59"
        report_json = get_report_json(start, end, message.chat.id)
        report = [hbold(f"📊 Отчет {year}-{month}\n")]
        report.append(hbold("📈 Доходы"))
        if report_json['incomes'] is not None and report_json['outcomes']:
            for inc in report_json['incomes']:
                report.append(f"👤 {inc['username']}: {inc['user_amount']} ({inc['percentage']})")
            report.append(hunderline(f"💰 Итого: {report_json['incomes_total_amount']}\n"))
            report.append(hbold("📉 Расходы"))
            for exp in report_json['outcomes']:
                report.append(f"{exp['type_name']}: {exp['type_amount']} ({exp['percentage']})")
            report.append(hunderline(f"💰 Итого: {report_json['outcomes_total_amount']}"))
            report.append(hbold(
                f"\n💸 Остаток: {round(report_json['incomes_total_amount'] - report_json['outcomes_total_amount'], 2)}"))
            await message.reply("\n".join(report))
        else:
            await message.reply('Необходимо заполнить доходы и расходы')

    else:
        print(message.date)
        last_day = calendar.monthrange(message.date.year, message.date.month)[-1]
        start = f"{message.date.year}-{message.date.month}-01 00:00:00"
        end = f"{message.date.year}-{message.date.month}-{last_day} 23:59:59"
        report_json = get_report_json(start, end, message.chat.id)
        report = [hbold(f"📊 Отчет {message.date.year}-{message.date.month}\n")]
        report.append(hbold("📈 Доходы"))
        if report_json['incomes'] is not None and report_json['outcome']:

            for inc in report_json['incomes']:
                report.append(f"👤 {inc['username']}: {inc['user_amount']} ({inc['percentage']})")
            report.append(hunderline(f"💰 Итого: {report_json['incomes_total_amount']}\n"))
            report.append(hbold("📉 Расходы"))
            for exp in report_json['outcome']:
                report.append(f"{exp['type_name']}: {exp['type_amount']} ({exp['percentage']})")
            report.append(hunderline(f"💰 Итого: {report_json['outcome_total_amount']}"))
            report.append(hbold(
                f"\n💸 Остаток: {round(report_json['incomes_total_amount'] - report_json['outcome_total_amount'], 2)}"))
            await message.reply("\n".join(report))
        else:
            await message.reply('Необходимо заполнить доходы и расходы')
