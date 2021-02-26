from migrations import migration


async def on_startup(dp):
    migration()


if __name__ == '__main__':
    from aiogram import executor
    from handlers.messages import dp

    executor.start_polling(dp, on_startup=on_startup)
