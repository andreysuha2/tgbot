from app.core.telegram import tg_client, tg_bot_dispatcher
from app.core.validator import validator
from app.core.poster import poster
from app.parsers import list
import asyncio

async def main():
    for parser in list:
        asyncio.create_task(parser.start())

    asyncio.create_task(validator.start())
    asyncio.create_task(poster.start())
    await tg_client.start()
    await tg_bot_dispatcher.start_polling()
