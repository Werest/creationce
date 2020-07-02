import telebot
import config as cg

bot = telebot.TeleBot(cg.TOKEN)

@bot.message_handler(commands=['start'])
def start_msg(msg):
    bot.send_message(msg.chat.id, cg.START_MSG)

@bot.message_handler(commands=['blank'])
def send_blank(msg):
    blank_doc = open('data/docs/Лист голосования.docx', 'rb')
    bot.send_document(msg.chat.id, blank_doc)

@bot.message_handler(content_types=['text'])
def all_messages(msg):
    # Получаем сообщение пользователя
    message = msg.text

    # Получаем Telegram id пользователя (очевидно, для каждого пользователя он свой)
    user_id = msg.chat.id

    # Отправляем сообщение
    bot.send_message(user_id, f"Вы написали: {message}")



# Запускаем бота, чтобы работал 24/7
if __name__ == '__main__':
    bot.polling(none_stop=True)
