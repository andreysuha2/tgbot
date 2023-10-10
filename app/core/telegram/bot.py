from aiogram import Bot
from aiogram.types import InputMediaDocument, InputMediaAudio, InputMediaPhoto, InputMediaVideo, FSInputFile
from app.core.config import config
from app.models.Message import Messages
from .Exceptions import TelegramBotCredentialsError
from functools import reduce

class TgBot(Bot):

    @property
    def media_types(self):
        return {
            "InputPhoto": { "cls": InputMediaPhoto, "type": "photo", "handler": self.send_photo },
            "InputAudio": { "cls": InputMediaAudio, "type": "audio", "handler": self.send_audio },
            "InputVideo": { "cls": InputMediaVideo, "type": "video", "handler": self.send_video },
            "InputDocument": { "cls": InputMediaDocument, "type": "document", "handler": self.send_document }
        }

    def __init__(self):
        self.__BOT_TOKEN = config.env.get("BOT_TOKEN")
        self.__CHENAL_ID = config.env.get("CHANEL_ID")
        if self.__BOT_TOKEN and self.__CHENAL_ID:
            super().__init__(self.__BOT_TOKEN)
        else:
            raise TelegramBotCredentialsError
        
    def create_media_item(self, type_id, path, caption=None):
        typeData = self.media_types.get(type_id)
        return typeData["cls"](type=typeData["type"], media=FSInputFile(path), caption=caption) if typeData else None

    async def post_message(self, message: Messages, chanel_id=None, reply_markup=None):
        current_chanel_id = chanel_id or self.__CHENAL_ID
        if message.text and not message.media:
            return await self.send_message(current_chanel_id, message.text, reply_markup=reply_markup)
        elif len(message.media) > 1:
            if message.text:
                message.media[0]["caption"] = message.text
            media_list = [ self.create_media_item(item["type"], item["path"], item.get("caption")) for item in message.media ]
            if not reply_markup:
                return await self.send_media_group(current_chanel_id, media=media_list)
            else:
                await self.send_media_group(current_chanel_id, media=media_list)
                return await self.send_message(current_chanel_id, 'Дії з попереднім повідомленням', reply_markup=reply_markup)
        else:
            media = message.media[0]
            media["caption"] = message.text or None
            handler = self.media_types[media["type"]]["handler"]
            file = FSInputFile(media["path"])
            return await handler(current_chanel_id, file, caption=media["caption"], reply_markup=reply_markup)