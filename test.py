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
        user_id = message.from_user.id if message.from_user else 'Unknown'
        chat_id = message.chat.id if message.chat else 'Unkown'
        logger.info(f'Starting {func.__name__} | User {user_id} | Chat: {chat_id}')

        try:
            result = func(message, *args, **kwargs)
            logger.info(f"Successful completed {func.__name__ } | User {user_id} | Chat: {chat_id}")
            return result

        except telebot.apihelper.ApiTelegramException as e:
            error_code = getattr(e, 'error_code', 'unknown')
            error_desc = getattr(e, 'description', str(e))

            if error_code == 403:
                logger.warning(f"User {user_id} block the bot")
            elif error_code == 429:
                logger.warning(f"Too may requests for user {user_id}")
            elif error_code == 400:
                logger.warning(f"Bad request: {error_desc}")
            else:
                logger.error(f"Telegram API error: {error_code} : {error_desc}")

            try:
                bot.send_message(chat_id, 'Error, try later')
            except:
                pass

        except telebot.apihelper.ApiException as e:
            logger.error(f"Api error in {func.__name__} : {e}")
            try:
                bot.send_message(chat_id, "Error to connect telegram")
            except:
                pass

        except ValueError as e:
            logger.warning(f'Validation error in {func.__name__} : {e}')
            try:
                bot.send_message(chat_id, f"Error with data: {e}")
            except:
                pass

        except FileNotFoundError as e:
            logger.error(f'File nor found in {func.__name__} : {e}')
            try:
                bot.send_messge(chat_id, "File not found")
            except:
                pass

        except Exception as e:
            logger.exception(f"Critical error in {func.__name__} : {e}")
            try:
                bot.send_message(chat_id, "Critical error")
            except:
                pass

        finally:
          logger.info(f'End {func.__name__} | User: {user_id} | Chat id: {chat_id}')
    return wrapper


@bot.message_handler(commands=['start'])
@handler_telegram_errors
def start_command(message):
    bot.reply_to(message, "Hi, im bot Kolbasenko")





'''
@bot.message_handler(commands=['start'])
@handler_telegram_errors
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
@handler_telegram_errors
def help_command(message):
    bot.reply_to(message, "Больште города")




@bot.message_handler(content_types=['photo'])
@handler_telegram_errors
def handle_photo(message):
    try:
        file_info = bot.get_file(message.photo[-1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)

        timestamp = datetime.now().strftime("%Y-%m-%d_-%H-%M-%S")
        filename = f"received_image_{message.from_user.id}_{timestamp}.jpg"
        save_path = os.path.join(Photo_Dir, filename)

        with open(save_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Image in hostage")
        logger.info(f'Photo save as: {filename}')



    except Exception as e:
        logger.error(f"Error in photo handler: {e}")
        raise


@bot.message_handler(commands=['sendphoto'])
@handler_telegram_errors
def send_photo(message):
    photos = os.listdir(Photo_Dir)

    if not photos:
        bot.reply_to(message, "You don't have saved photos")
        return

    latest_photo = sorted(photos)[-1]
    photo_path = os.path.join(Photo_Dir, latest_photo)
    with open(photo_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption={latest_photo})




@bot.message_handler(conent_types=["video"])
@handler_telegram_errors
def handle_video(message):
    file_info = bot.get_file(message.video.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_-%H-%M-%S")
    save_path = os.path.join(Photo_Dir, f"recived_video_{message.from_user.id}_{timestamp}.mp4")

    with open(save_path, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "save your stupid video")


@bot.message_handler(commands=['sendvideo'])
@handler_telegram_errors
def send_video(message):
    video = open(" ", 'rb')
    bot.send_video(message.chat.id, video)





@bot.message_handler(content_types=['document'])
@handler_telegram_errors
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    timestamp = datetime.now().strftime("%Y-%m-%d_-%H-%M-%S")

    
    with open(message.document.file_name, 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.reply_to(message, "save epstein files")


@bot.message_handler(commands=['senddocuments'])
@handler_telegram_errors
def send_document(message):
    document = open('', 'rb')
    bot.send_document(message.chat.id, document)


@bot.message_handler(content_types=['location'])
@handler_telegram_errors
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