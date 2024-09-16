import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import ephem
import datetime
from random import randint, choice
import My_settings
from glob import glob

# настроим модуль ведения журнала логов
logging.basicConfig(
    filename = "MyBot.log",
    level=logging.INFO
)

# определяем асинхронную функцию
async def start(update, context):
    
    # ожидание отправки сообщения по сети - нужен `await`
    await context.bot.send_message(chat_id=update.effective_chat.id, 
                                   text="I'm a bot, please talk to me!")


async def talk_to_me(update, context):
    text_ = update.message.text
    print(text_)
    await context.bot.send_message( chat_id=update.effective_chat.id, text=text_)
    


async def moon(update, context):
    data_ = update.message.text.split()[1].split('/')
    text_ = ephem.next_full_moon(datetime.date(int(data_[0]),int(data_[1]),int(data_[2])))
    await context.bot.send_message( chat_id=update.effective_chat.id, text=f'{text_}')


async def guess_number(update, context):
    if context.args:
        try:
            number = int(context.args[0])
            message = (f"Вы ввели число{number}")
        except(TypeError, ValueError):
            message = 'Введите целое число'            
    else:
        message = 'Введите целое число'
    await context.bot.send_message( chat_id=update.effective_chat.id, text=message)
    message = rand_num_comp(number)     
    await context.bot.send_message( chat_id=update.effective_chat.id, text=message)

def rand_num_comp(user_number):
    comp_number = randint(user_number-10, user_number+10)
    if user_number > comp_number:
        message = f'Ты загадал {user_number}, я загадал {comp_number}, ты выиграл!'
    elif user_number == comp_number:
        message = f'Ты загадал {user_number}, я загадал {comp_number}, ничья!'
    else:      
        message = f'Ты загадал {user_number}, я загадал {comp_number}, я выиграло!'
    return message



async def photo(update, context):
    images = glob('Photo/*.jfif')
    print(images)
    image = choice(images)
    await context.bot.send_photo( chat_id=update.effective_chat.id, photo = open(image, 'rb') )


if __name__ == '__main__':
    TOKEN = My_settings.API_KEY
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()

    logging.info("Bot started")
    # создаем обработчик для команды '/start'
    start_handler = CommandHandler('start', start)
    
    next_full_moon = CommandHandler('next_full_moon', moon)

    guess_number_game = CommandHandler('guess', guess_number)
    
    
    # регистрируем обработчик в приложение
    application.add_handler(start_handler)
    application.add_handler(next_full_moon)
    application.add_handler(guess_number_game)
    application.add_handler(CommandHandler('ursdon', photo))
    application.add_handler(MessageHandler(filters.TEXT, talk_to_me))
    
    # запускаем приложение    
    application.run_polling()