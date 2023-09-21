from app.models import Message, MessageStatus
from app.core.poster import poster
from app.core.config import config
from datetime import datetime, timedelta
from app.core.config import config
from mongoengine.queryset.visitor import Q
import spacy
import asyncio

class Validator:
    max_days_for_compare = config.app.validator.max_days_for_compare
    nlp = spacy.load(config.app.validator.spacy_model)
    similarity_coef = config.app.validator.similarity_coef

    def __init__(self) -> None:
        self.__queue = asyncio.Queue()

    async def add_message(self, message: Message) -> None:
        await self.__queue.put(message)

    def __validate(self, message: Message) -> None:
        message.status = MessageStatus.ON_VALIDATE
        message.save()
        raw = { "timestamp": { "$gte": datetime.now() - timedelta(days=self.max_days_for_compare) } }
        messages = Message.objects(
            Q(__raw__=raw) & (
                Q(status=MessageStatus.DECLINE) |
                Q(status=MessageStatus.POSTED) |
                Q(status=MessageStatus.PENDING_FOR_POST)
            )
        )
        similarity = 0
        for m in messages:
            nlp_m = self.nlp(m.text)
            nlp_message = self.nlp(message.text)
            current_similarity = nlp_message.similarity(nlp_m)
            if current_similarity > similarity:
                similarity = current_similarity
        return similarity < self.similarity_coef
    
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