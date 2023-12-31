import asyncio
import logging
import os
import dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router
#from config import TB_TOKEN
from tg_analytic import db_start
import locale

# aiogram==3.0.0b7

locale.setlocale(locale.LC_ALL, '')

dotenv.load_dotenv()

db_start()

async def main():
    bot = Bot(token=os.getenv('TB_TOKEN'), parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot=bot, storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

#keep_alive()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
