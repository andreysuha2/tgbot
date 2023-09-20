from app.core.message import Message
from app.core.poster import poster
import asyncio

class Validator:
    def __init__(self) -> None:
        self.__queue = asyncio.Queue()

    async def add_message(self, message: Message) -> None:
        await self.__queue.put(message)

    def __validate(self, message: Message) -> None:
        return True
    
    async def __worker(self) -> None:
        message = await self.__queue.get()
        if self.__validate(message):
            await poster.put(message)
        self.__queue.task_done()

    async def start(self) -> None:
        while True:
            await asyncio.sleep(5)
            if not self.__queue.empty():
                asyncio.create_task(self.__worker())

validator = Validator()