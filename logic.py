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

@bot.message_handler(commands=['version'])
def start_msg(msg):
    bot.send_message(msg.chat.id, cg.version)

@bot.message_handler(content_types=['text'])
def all_messages(msg):
    message = msg.text
    user_id = msg.chat.id
    bot.send_message(user_id, f"Вы написали: {message}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
