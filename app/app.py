from app.core.config import config
from telethon import events
from app.core.telegram import tg_client, tg_bot_dispatcher
from app.core.queue import queue
import asyncio

async def main():
    source = [ 'https://t.me/super_test_chanel2', 'https://t.me/super_test_chanel' ]

    @tg_client.on(events.NewMessage(chats=source))
    async def handler(event):
        #print(event, event.raw_text)
        #await tg_bot.send_message(event.raw_text)
        print(event.raw_text)
        await queue.put(event.raw_text)

    asyncio.create_task(queue.start())
    await tg_client.start()
    await tg_bot_dispatcher.start_polling()
