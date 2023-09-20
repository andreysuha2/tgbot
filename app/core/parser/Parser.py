from app.core.queue import queue
from app.core.message import Message
from typing import Optional

class Parser:
    def __init__(self, source: str) -> None:
        self.source = source

    def start(self) -> None:
        pass

    def create_message(self, *args, **kargs) -> None:
        return Message(self.source, *args, **kargs)
    
    async def load_message(self, data) -> Optional[Message]:
        pass

    async def handle_message(self, data) -> None:
        message = self.load_message(data)
        if message:
            await queue.put(message)