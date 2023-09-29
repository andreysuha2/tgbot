from app.core.telegram import tg_client, tg_bot, tg_bot_dispatcher
from app.core.validator import validator
from app.core.poster import poster
from app.parsers import list
from app.routes.user import router as user_router
import asyncio

async def main():
    for parser in list:
        asyncio.create_task(parser.start())

    tg_bot_dispatcher.include_routers(user_router)
    asyncio.create_task(validator.start())
    asyncio.create_task(poster.start())
    await tg_client.start()
    await tg_bot_dispatcher.start_polling(tg_bot)
