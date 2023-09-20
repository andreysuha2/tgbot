from aiogram import Bot
from app.core.config import config
from .Exceptions import TelegramBotCredentialsError

class TgBot(Bot):
    def __init__(self):
        self.__BOT_TOKEN = config.get("BOT_TOKEN")
        self.__CHENAL_ID = config.get("CHANEL_ID")
        if self.__BOT_TOKEN and self.__CHENAL_ID:
            super().__init__(self.__BOT_TOKEN)
        else:
            raise TelegramBotCredentialsError

    async def send_message(self,*args, **kargs):
        return await super().send_message(self.__CHENAL_ID, *args, **kargs)