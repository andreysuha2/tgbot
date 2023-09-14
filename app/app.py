from telebot import TeleBot
from app.config import config

BOT = TeleBot(config.get("BOT_TOKEN"))

def main():
    @BOT.message_handler(commands=["start", "help"])
    def hello(message):
        pass