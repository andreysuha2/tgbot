import telebot
bot = telebot.TeleBot('6470527316:AAEFytM5WygVlFZFW94WeGIwOLr0wNHieC4', parse_mode=None)

@bot.message_handler(commands=[ 'start', 'help' ])
def message_handler(message):
    bot.reply_to(message, 'Hi, i am bot')

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	bot.reply_to(message, message.text)
      
bot.infinity_polling()