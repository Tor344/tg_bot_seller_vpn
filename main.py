import asyncio
import sys
import logging

from bot.apps.payments.handlers import router as payments_router
from bot.apps.shopping_showcase.handlers import router as shopping_showcase_router
from aiogram import Bot, Dispatcher

from bot.core.scheduler import scheduler, up_data_database

import config.settings as set

from bot.apps.start.handlers import router as start_router
from bot.apps.user.handlers import router as user_router
from bot.apps.admin.handlers import router as admin_router

from bot.database.core import db


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    stream=sys.stdout
)


logger = logging.getLogger(__name__)


bot = Bot(token=set.API_TOKEN)
dp = Dispatcher()
dp.include_router(payments_router)

dp.include_router(shopping_showcase_router)
dp.include_router(user_router)
dp.include_router(admin_router)
dp.include_router(start_router)


async def main():
    try:
        await db.connect()
        logger.info("Бот запущен")
        scheduler.add_job(
        up_data_database,
        trigger="cron",
        hour=18,
        minute=5,
        args=[bot],  # bot пойдёт в параметр функции
    )

        scheduler.start()

        await dp.start_polling(bot)

    except Exception as e:
        logger.error(f"Ошибка при запуске: {e}")

    finally:
        await db.close()




if __name__ == "__main__":
    asyncio.run(main())