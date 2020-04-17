# bot.py

# import required libraries
import telebot
import requests

# import environ to get token and project name from .env
from os import environ 

# setup bot with Telegram token from .env
bot = telebot.TeleBot(environ['TELEGRAM_TOKEN']) 

# handler triggered with the /start command
@bot.message_handler(commands=['start'])

def send_welcome(message):
    bot.reply_to(message, 'hi there') 
    
# configure the webhook for the bot, with the url of the Glitch project
bot.set_webhook("https://{}.glitch.me/{}".format(environ['PROJECT_NAME'], environ['TELEGRAM_TOKEN']))
