from app.models import Message, MessageStatus
from app.core.validator import validator
from mongoengine.queryset.visitor import Q

class MessageController:
    def _get_message(self, message_id):
        return Message.objects(Q(id=message_id) & Q(status=MessageStatus.ON_HUMAN_VALIDATE)).first()

    async def accept_message(self, clb, message_id):
        message = self._get_message(message_id)
        answer = "Повідомлення вже оброблене"
        if message:
            await validator.moderator_accept_message(message)
            answer = "Повідомлення відправлене на публікацію"
        await clb.answer(answer)

    async def decline_message(self, clb, message_id):
        message = self._get_message(message_id)
        answer = "Повідомлення вже оброблене"
        if message:
            validator.moderator_decline_message(message)
            answer = "Повідомлення відхилено"
        await clb.answer(answer)

message_controller = MessageController()