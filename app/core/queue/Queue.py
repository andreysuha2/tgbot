import asyncio
from app.core.telegram import tg_bot

class Queue:
    def __init__(self) -> None:
        self.__queue = asyncio.Queue()

    async def _worker(self):
        message = await self.__queue.get()
        await tg_bot.send_message(message)
        self.__queue.task_done()

    async def put(self, item):
        return await self.__queue.put(item)
    
    async def start(self):
        while True:
            await asyncio.sleep(5)
            if not self.__queue.empty():
                asyncio.create_task(self._worker())
        

queue = Queue()