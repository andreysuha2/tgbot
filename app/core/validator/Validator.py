from app.models import Message, MessageStatus
from app.core.poster import poster
from app.core.config import config
import asyncio

class Validator:
    def __init__(self) -> None:
        self.__queue = asyncio.Queue()

    async def add_message(self, message: Message) -> None:
        await self.__queue.put(message)

    def __validate(self, message: Message) -> None:
        message.status = MessageStatus.ON_VALIDATE
        message.save()
        return True
    
    async def __worker(self) -> None:
        message = await self.__queue.get()
        if self.__validate(message):
            message.status = MessageStatus.PENDING_FOR_POST
            await poster.put(message)
        else:
            message.status = MessageStatus.DECLINE
        message.save()
        self.__queue.task_done()

    async def start(self) -> None:
        while True:
            await asyncio.sleep(config.app.validator.sleep)
            if not self.__queue.empty():
                asyncio.create_task(self.__worker())

validator = Validator()