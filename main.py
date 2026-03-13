import asyncio
from threading import Thread

from src.sim868_cmd import check_unread_message, setup_module
from src.sim868_cmd_queue import receive_cmd_loop, request_check_message_event
from src.sim868_pwrkey import check_and_enable_gsm_module
from src.telegram_bot import send_message
from src.telegram_bot_handler import start_bot_polling


async def main():
    await send_message("🚀 Бот запущен...")
    await check_and_enable_gsm_module()

    Thread(target=receive_cmd_loop, args=[]).start()

    try:
        await setup_module()
        await check_unread_message()
    except Exception as error:
        await send_message("🛑 Ошибка: " + str(error))
        raise error

    bot_task = asyncio.create_task(start_bot_polling())

    try:
        while True:
            print("Waiting for messages...")
            request_check_message_event.wait(timeout=10)
            await check_unread_message()
            request_check_message_event.clear()
    finally:
        bot_task.cancel()
        try:
            await bot_task
        except asyncio.CancelledError:
            pass


if __name__ == "__main__":
    asyncio.run(main())
