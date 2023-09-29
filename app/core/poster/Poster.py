import asyncio
from app.core.telegram import tg_bot
from app.core.config import config
from app.models import MessageStatus

class Poster:
    def __init__(self) -> None:
        self.__queue = asyncio.Queue()

    async def _worker(self):
        message = await self.__queue.get()
        await tg_bot.post_message_to_chanel(message.text)
        message.status = MessageStatus.POSTED
        message.save()
        self.__queue.task_done()

    async def put(self, item):
        return await self.__queue.put(item)
    
    async def start(self):
        while True:
            await asyncio.sleep(config.app.poster.sleep)
            if not self.__queue.empty():
                asyncio.create_task(self._worker())
        

poster = Poster()