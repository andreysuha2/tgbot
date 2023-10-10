from app.models import Message
from app.core.parser import Parser
from app.core.telegram import tg_client
from app.core.config import config
from telethon import events, utils
from telethon.tl.types import MessageMediaDocument, MessageMediaPhoto
from aiogram.methods import get_file
class TelegramParser(Parser):
    def __init__(self) -> None:
        super().__init__("telegram")
        self.chanels = config.app.parsers.telegram_chanels
    
    async def start(self) -> None:
        @tg_client.on(events.NewMessage(chats=self.chanels))
        async def handler(event: events.NewMessage.Event):
            await self.handle_message(event)

    async def _parse_event(self, event: events.NewMessage.Event):
        media = []
        if event.message.media:
            file_path = await self.temporary_store_file(event.media)
            data = utils.get_input_media(event.message).to_dict()["id"]
            media.append({ "type": data["_"], "id": data["id"], "path": file_path })
        return {
            "source_id": str(event.chat_id),
            "message_id": str(event.message.id),
            "text": event.raw_text,
            "group_id": event.message.grouped_id,
            "media": media
        }

    async def load_message(self, event) -> Message:
        message = None
        message_data = await self._parse_event(event)
        if event.message.grouped_id:
            message = Message.objects(group_id=event.message.grouped_id).first()
            if message and event.message.media:
                message.media.append(message_data["media"][0])
                if message_data["text"]:
                    message.text = message_data["text"]
                message.save()
                return
        if not message:
            message = self.create_message(**message_data)
        return message