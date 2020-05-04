### bot.py



import telebot
import requests
import imgProcessor as iproc
from os import environ 



## Setup bot with Telegram token from .env
bot = telebot.TeleBot(environ['TELEGRAM_TOKEN'])


## Basic handler triggered with the /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 'hi there')
    
    
## Image processing handler
proc_cmds = iproc.get_proc_cmds()
@bot.message_handler(content_types=['text', 'photo'])
def process_photo(message):
  
    # get chat ID and message contents
    chat_id = message.chat.id
    msg_capt = message.caption
    msg_text = message.text
    msg_img = message.photo
    
    if msg_capt:
        msg_text = msg_capt
    
    msg_words = []
    if msg_text:
        msg_words = msg_text.split(' ')
    
    # send error message if no image or no caption
    if msg_words[0] in proc_cmds and not msg_img:
        bot.send_message(chat_id, 'Please, provide an image ._.')
    elif msg_img and not msg_text:
        bot.send_message(chat_id, 'Please, provide a command ._.')
    elif msg_img and not msg_words[0] in proc_cmds:
        bot.send_message(chat_id, 'Invalid command .__.')
    
    # process if all is ok
    elif msg_img and msg_words[0] in proc_cmds:
        proc_cmd = msg_words[0]
        proc_args = []
        if len(msg_words) > 1:
            proc_args = msg_words[1:]
        file_id = msg_img[-1].file_id
        img_info = bot.get_file(file_id)
        img_byte = bot.download_file(img_info.file_path)
        img_byte_new, errors, log = iproc.process_byte(img_byte, proc_cmd, proc_args)
        if errors:
            bot.send_message(chat_id, log, reply_to_message_id=message.message_id)
        else:
            bot.send_photo(chat_id, img_byte_new, reply_to_message_id=message.message_id)
        
        
    
## Configure the webhook for the bot with the url of the Glitch project
bot.set_webhook("https://{}.glitch.me/{}".format(environ['PROJECT_NAME'], environ['TELEGRAM_TOKEN']))