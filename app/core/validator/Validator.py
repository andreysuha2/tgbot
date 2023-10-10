from app.models import Message, MessageStatus, User, UserRole
from app.core.poster import poster
from app.core.config import config
from datetime import datetime, timedelta
from app.core.config import config
from mongoengine.queryset.visitor import Q
from app.core.telegram import tg_bot
from aiogram import types
from app.callbacks_factorys.message_callbacks import AcceptMessageCallbackFactory
import spacy
import asyncio

class Validator:
    max_days_for_compare = config.app.validator.max_days_for_compare
    nlp = spacy.load(config.app.validator.spacy_model)
    similarity_coef = config.app.validator.similarity_coef

    def __init__(self) -> None:
        self.__queue = asyncio.Queue()

    def _get_accept_message_buttons(self, message_id) -> types.InlineKeyboardMarkup:
        buttons = [
            [
                types.InlineKeyboardButton(
                    text='Опублікувати',
                    callback_data=AcceptMessageCallbackFactory(action="accept", message_id=message_id).pack()
                ),
                types.InlineKeyboardButton(
                    text='Відхилити',
                    callback_data=AcceptMessageCallbackFactory(action="decline", message_id=message_id).pack()
                )
            ]
        ]
        return types.InlineKeyboardMarkup(inline_keyboard=buttons)

    async def send_to_human_validation(self, message: Message):
        moderators: list[User] = User.objects(Q(role=UserRole.ADMIN) | Q(role=UserRole.MODERATOR))
        for moderator in moderators:
            await tg_bot.post_message(
                message,
                chanel_id=moderator.user_id,
                reply_markup=self._get_accept_message_buttons(str(message.id))
            )

    async def moderator_accept_message(self, message: Message):
        message.status = MessageStatus.PENDING_FOR_POST
        message.save()
        await poster.put(message)
        

    def moderator_decline_message(self, message: Message):
        message.status = MessageStatus.DECLINED_BY_HUMAN
        message.save()    

    async def add_message(self, message: Message) -> None:
        await self.__queue.put(message)

    def __validate(self, message: Message) -> None:
        message.status = MessageStatus.ON_AI_VALIDATE
        message.save()
        raw = { "timestamp": { "$gte": datetime.now() - timedelta(days=self.max_days_for_compare) } }
        messages = Message.objects(
            Q(__raw__=raw) & (
                Q(status=MessageStatus.DECLINED_BY_AI) |
                Q(status=MessageStatus.POSTED) |
                Q(status=MessageStatus.PENDING_FOR_POST)
            )
        )
        similarity = 0
        if not message.text:
            return True
        for m in messages:
            nlp_m = self.nlp(m.text)
            nlp_message = self.nlp(message.text)
            current_similarity = nlp_message.similarity(nlp_m)
            if current_similarity > similarity:
                similarity = current_similarity
        return similarity < self.similarity_coef
    
    async def __worker(self) -> None:
        message_id = await self.__queue.get()
        message = Message.objects(id=message_id).first()
        if self.__validate(message):
            message.status = MessageStatus.ON_HUMAN_VALIDATE
            await self.send_to_human_validation(message)
        else:
            message.status = MessageStatus.DECLINED_BY_AI
        message.save()
        self.__queue.task_done()

    async def start(self) -> None:
        while True:
            await asyncio.sleep(config.app.validator.sleep)
            if not self.__queue.empty():
                asyncio.create_task(self.__worker())

validator = Validator()