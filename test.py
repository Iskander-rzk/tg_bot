import telebot
import os
import logging
import functools
from dotenv import load_dotenv
from datetime import datetime


load_dotenv()
Token = os.getenv("TOKEN")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(Token)

#Настройка папок
Base_Dir = os.path.dirname(os.path.abspath(__file__))
Downloads_Dir = os.path.join(Base_Dir, 'downloads')

Photo_Dir = os.path.join(Downloads_Dir, 'photo')
Video_Dir = os.path.join(Downloads_Dir, 'video')
Docs_Dir = os.path.join(Downloads_Dir, 'documents')


#функция для обработок ошибок
def handler_telegram_errors(func):
    @functools.wraps(func)
    def wrapper(message, bot=None, *args, **kwargs):
        current_bot = bot or globals().get('bot')
        logger.info(f'Starting {func.__name__} for user {message.chat.id}')

        try:
            result = func(message, *args, **kwargs)

            logger.info(f"Successful completed {func.__name__ } for user {message.chat.id}")
            return result
        except telebot.apihelper.ApiException as e:
            logger.error(f"Telegram API errror: {e}")
            try:
                bot.send_message(message.chat.id, 'Message failed to send')
            except:
                pass
        except Exception as e:
            logger.exception(f'Unexpected error: {e}')
            try:
                bot.send_message(message.chat.id, 'Unkown error')
            except:
                pass
    return wrapper


@bot.message_handler(commands=['start'])
@handler_telegram_errors
def start_command(message):
    bot.reply_to(message, "Hi, im bot Kolbasenko")





'''
@bot.message_handler(commands=['start'])
def start_command(message):
    try:
        #логгируем получение комнды /start
        logger.info('get command /start from user %s', message.chat.id)
        #отправляем приветсвие пользователю
        bot.reply_to(message,"Hi, im bot Kolbasenko")
    except telebot.apihelper.ApiException as e:
        #логируем ошибкупри взаимодействии c API Telegram
        logger.error('Message failed to send %s', e)
        bot.send_message(message.chat.id, 'Error sending message. Please try later.')
    except Exception as e:
        logger.exception('Unkown error: %s', e)
        bot.send_message(message.chat.id, "Unkown error. Please try later")
    else:
        logger.info('Message successful send to user %s', message.chat.id)
    finally:
        logger.info("End process command /start for user %s", message.chat.id)

'''




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



'''
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, "hi, what are hell do you want!?")

    keyboard = types.InlineKeyboardMarkup(row_width=2)

    button1 = types.InlineKeyboardButton('Red pill', callback_data='data1')
    button2 = types.InlineKeyboardButton('Blue pill', callback_data='data2')

    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, 'Choase the pill Neo', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def handler(call):
    bot.answer_callback_query(call.id)
    if call.data == 'data1':
        bot.send_message(call.message.chat.id, "Это была барбариска")
    elif call.data == 'data2':
        bot.send_message(call.message.chat.id, 'Это была стиральная капсула')
        
        

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.reply_to(message, 'what are hell do you want!?')

    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)

    button1 = types.KeyboardButton('Red')
    button2 = types.KeyboardButton('Blue')

    keyboard.add(button1, button2)

    bot.send_message(message.chat.id, 'Chose the pill:', reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def handler_text(message):
    if message.text == 'Red':
        bot.send_message(message.chat.id, 'Это была барбариска')
    elif message.text == 'Blue':
        bot.send_message(message.chat.id, 'Это была стиральная капсула')
    else:
        bot.send_message(message.chat.id, 'Это был мухамор')





@bot.message_handler(content_types=['text'])
def handle_text(message):
    response = f"Вы написали: {message.text}"
    bot.send_message(message.chat.id, response)
'''


bot.polling()