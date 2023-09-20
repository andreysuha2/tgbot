from app.core.message import Message
from app.core.parser import Parser
from app.core.telegram import tg_client
from app.core.config import config
from telethon import events

class TelegramParser(Parser):
    def __init__(self) -> None:
        super().__init__("telegram")
        self.chanels = config.app.parsers.telegram_chanels
    
    async def start(self) -> None:
        @tg_client.on(events.NewMessage(chats=self.chanels))
        async def handler(event):
            await self.handle_message(event)

    def load_message(self, event) -> Message:
        return self.create_message(event.chat_id, event.message.id, event.raw_text)