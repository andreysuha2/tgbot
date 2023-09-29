from app.core.validator import validator
from app.models import Message
from typing import Optional

class Parser:
    def __init__(self, source: str) -> None:
        self.source = source

    def start(self) -> None:
        pass

    def create_message(self, source_id, message_id, text) -> Message:
        message = Message(
            source=str(self.source),
            source_id=str(source_id),
            message_id=str(message_id),
            text=text
        )
        message.save()
        return message
    
    async def load_message(self, data) -> Optional[Message]:
        pass

    async def handle_message(self, data) -> None:
        message = self.load_message(data)
        if message:
            await validator.add_message(message)