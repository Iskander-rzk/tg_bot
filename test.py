import telebot
import os
from dotenv import load_dotenv
from datetime import datetime
from telebot import types

load_dotenv()
Token = os.getenv("TOKEN")


bot = telebot.TeleBot(Token)

#Настройка папок
Base_Dir = os.path.dirname(os.path.abspath(__file__))
Downloads_Dir = os.path.join(Base_Dir, 'downloads')

Photo_Dir = os.path.join(Downloads_Dir, 'photo')
Video_Dir = os.path.join(Downloads_Dir, 'video')
Docs_Dir = os.path.join(Downloads_Dir, 'documents')


#@bot.message_handler(commands=['start'])
#def start_command(message):
#    bot.reply_to(message,"Hi, im bot Kolbasenko")


@bot.message_handler(commands=['help', 'about'])
def help_command(message):
    bot.reply_to(message, "Больште города")




@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_-%H-%M-%S")
    save_path = os.path.join(Photo_Dir, f"received_image_{message.from_user.id}_{timestamp}.jpg")

    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)
    bot.reply_to(message, "Image in hostage")


@bot.message_handler(commands=['sendphoto'])
def send_photo(message):
    photo = open('/home/alex/PycharmProjects/tg_bot/received_image.jpg', 'rb')
    bot.send_photo(message.chat.id, photo)





@bot.message_handler(conent_types=["video"])
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_-%H-%M-%S")
    save_path = os.path.join(Photo_Dir, f"recived_video_{message.from_user.id}_{timestamp}.mp4")

    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "save your stupid video")


@bot.message_handler(commands=['sendvideo'])
def send_video(message):
    video = open(" ", 'rb')
    bot.send_video(message.chat.id, video)





@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_-%H-%M-%S")

    
    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "save epstein files")


@bot.message_handler(commands=['senddocuments'])
def send_document(message):
    document = open('', 'rb')
    bot.send_document(message.chat.id, document)


@bot.message_handler(content_types=['location'])
def geo_location(message):
    gif = open('/home/alex/PycharmProjects/tg_bot/clash-royale-rocket.gif', 'rb')
    bot.send_animation(message.chat.id, gif)





#Создание InlineKeyboardMarkup




@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "hi, what are hell do you want!?")

    keyboard = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton('Red pill', callback_data='data1')
    button2 = types.InlineKeyboardButton('Blue pill', callback_data='data2')

    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, 'Choase the pill Neo', reply_markup=keyboard)




#@bot.message_handler(content_types=['text'])
#def handle_text(message):
#    response = f"Вы написали: {message.text}"
#    bot.send_message(message.chat.id, response)

bot.polling()