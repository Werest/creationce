import telebot
import config as cg
import datetime
import dbworker
import psycopg2

now = datetime.datetime.now()
bot = telebot.TeleBot(cg.TOKEN)

def dbpg(kv):
    conn = psycopg2.connect(dbname=cg.dbname, user=cg.user, password=cg.password, host=cg.host)

    cursor = conn.cursor()
    cursor.execute("Select name from schema_zhya.table where kv= %(kv)s", {'kv': kv})
    records = cursor.fetchall()
    cursor.close()
    conn.close()
    try:
        return records[0]
    except:
        return "___"


@bot.message_handler(commands=['start'])
def start_msg(msg):
    bot.send_message(msg.chat.id, cg.START_MSG)


@bot.message_handler(commands=['version'])
def start_msg(msg):
    bot.send_message(msg.chat.id, cg.VERSION)


@bot.message_handler(commands=['water'])
def readIndicationsHotColdWater(msg):
    date_now = now.strftime("%d-%m-%Y %H:%M")
    bot.send_message(msg.chat.id, date_now)
    bot.send_message(msg.chat.id, cg.TAKE_NUMBER_PLACE)
    dbworker.set_state(msg.chat.id, cg.State.NUMBER_PLACE.value)


@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == cg.State.NUMBER_PLACE.value)
def user_entering_name(message):
    cg.NUMBER_PLACE = message.text
    bot.send_message(message.chat.id, 'Ваш номер квартиры: %s' % message.text)
    bot.send_message(message.chat.id, cg.WHICH_FIO)
    dbworker.set_state(message.chat.id, cg.State.FIO.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == cg.State.FIO.value)
def user_entering_name(message):
    fio_msg = message.text
    if fio_msg in dbpg(int(cg.NUMBER_PLACE)):
        bot.send_message(message.chat.id, 'ФИО проверено, всё в порядке')
        bot.send_message(message.chat.id, cg.HOT_WATER_INDICATOR)
        dbworker.set_state(message.chat.id, cg.State.HOT_WATER.value)
    else:
        bot.send_message(message.chat.id, "Неверное ФИО!")
        dbworker.set_state(message.chat.id, cg.State.S_START.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == cg.State.HOT_WATER.value)
def user_entering_name(message):
    msg = message.text
    bot.send_message(message.chat.id, cg.HOT_WATER_YOU % msg)
    bot.send_message(message.chat.id, cg.COLD_WATER_INDICATOR)
    dbworker.set_state(message.chat.id, cg.State.COLD_WATER.value)

@bot.message_handler(func=lambda message: dbworker.get_current_state(message.chat.id) == cg.State.COLD_WATER.value)
def user_entering_name(message):
    msg = message.text
    bot.send_message(message.chat.id, cg.COLD_WATER_YOU % msg)
    bot.send_message(message.chat.id, "Показания записаны. Спасибо!")
    # dbworker.set_state(message.chat.id, cg.State.COLD_WATER.value)


@bot.message_handler(content_types=['text'])
def all_messages(msg):
    message = msg.text
    user_id = msg.chat.id
    bot.send_message(user_id, f"Вы написали: {message}")


if __name__ == '__main__':
    bot.polling(none_stop=True)
