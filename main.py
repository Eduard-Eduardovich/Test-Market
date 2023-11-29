import aiogram
import asyncio 
import os
from aiogram import Router, F
from aiogram import Bot, Dispatcher,types
from dotenv import load_dotenv
from handlers import handler
from models import async_main



       
async def main():
    await async_main()
    
    load_dotenv('.env')
    token = os.getenv("TOKEN")
    bot = Bot(token,parse_mode='HTML')
    dp = Dispatcher()

    dp.include_routers(handler.router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())