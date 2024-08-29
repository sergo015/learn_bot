import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import My_settings

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

if __name__ == '__main__':
    TOKEN = API_KEY
    # создание экземпляра бота через `ApplicationBuilder`
    application = ApplicationBuilder().token(TOKEN).build()

    logging.info("Bot started")
    # создаем обработчик для команды '/start'
    start_handler = CommandHandler('start', start)
    
    
    # регистрируем обработчик в приложение
    application.add_handler(start_handler)
    application.add_handler(MessageHandler(filters.TEXT, talk_to_me))
    
    # запускаем приложение    
    application.run_polling()