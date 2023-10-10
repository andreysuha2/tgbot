from app.core.validator import validator
from app.models import Message
from app.core.config import config
from typing import Optional
from app.definitions import ROOT_DIR
from datetime import datetime
from app.core.telegram import tg_client

class Parser:
    temp_folder = f"{ROOT_DIR}/{config.app.files.temp_folder}"
    file_counter = 0

    def __init__(self, source: str) -> None:
        self.source = source

    def start(self) -> None:
        pass

    async def temporary_store_file(self, file):
        self.file_counter += 1
        temp_dir = f"{self.temp_folder}/{int(datetime.now().timestamp() + self.file_counter)}"
        return await tg_client.download_media(file, file=temp_dir)

    def create_message(self, **kargs) -> Message:
        source_id, message_id = kargs["source_id"], kargs["message_id"]
        message = Message.objects(source=self.source, source_id=source_id, message_id=message_id)
        if not message:
            message = Message(source=self.source, **kargs)
            message.save()
            return message
        return None
    
    async def load_message(self, data) -> Optional[Message]:
        pass

    async def handle_message(self, data) -> None:
        message = await self.load_message(data)
        if message:
            await validator.add_message(message.id)