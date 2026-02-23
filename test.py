import telebot
import time
from datetime import datetime

bot = telebot.TeleBot('733261376:AAH4AqKJQgT_WNEserRXM-qzhKVNZHYbGmI')

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message,"Hi, im bot Kolbasenko")


@bot.message_handler(commands=['help', 'about'])
def help_command(message):
    bot.reply_to(message, "Больште города")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_-%H-%M-%S")
    photoname = f"received_image_{timestamp}.jpg"

    with open(photoname, 'wb') as new_file:
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
    videoname = f"recived_video_{timestamp}.mp4"

    with open(videoname, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "save your stupid video")


@bot.message_handler(commands=['sendvideo'])
def sendvideo(message):
    video = open(" ", 'rb')
    bot.send_video(message.chat.id, video)




#@bot.message_handler(content_types=['text'])
#def handle_text(message):
#    response = f"Вы написали: {message.text}"
#    bot.send_message(message.chat.id, response)

bot.polling()