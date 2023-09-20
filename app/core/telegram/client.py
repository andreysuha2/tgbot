from app.core.config import config
from telethon import TelegramClient
from .Exceptions import TelegramClientCredentialsError

class TgClient(TelegramClient): 
    def __init__(self) -> None:
        self.__API_ID = config.env.get("TELEGRAM_API_ID")
        self.__API_HASH = config.env.get("TELEGRAM_API_HASH")
        self.__API_SESSION_NAME = config.env.get("TELEGRAM_API_SESSION_NAME", "tgsession")
        if self.__API_HASH and self.__API_ID and self.__API_SESSION_NAME:
            super().__init__(self.__API_SESSION_NAME, self.__API_ID, self.__API_HASH)
        else:
            raise TelegramClientCredentialsError
        