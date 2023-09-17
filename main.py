import telebot
import sqlite3
from telebot import types
bot = telebot.TeleBot('6630395700:AAEPNADLVlfc7HvH01pPDWJ81w5vAP4TNQw')
print('The server is running')


# keyboards
def first_level_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    # Сюда добавишь оставшиеся кнопки первого уровня
    keyboard.add("☃ Python", "☠ С++", "☹ Javascript", "❄ Профиль")
    return keyboard


# database
def create_database(message):
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            python_first_test INTEGER,
            python_second_test INTEGER,
            c_first_test INTEGER,
            c_second_test INTEGER
        )""")
    connect.commit()

    u_chat_id = message.chat.id
    cursor.execute(f'SELECT id FROM users WHERE id = {u_chat_id}')
    data = cursor.fetchone()
    if data is None:
        u_id = [message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name,
                0, 0, 0, 0]
        cursor.execute(
            'INSERT INTO users (id, username, first_name, last_name, python_first_test, python_second_test, c_first_test, c_second_test) VALUES (?, ?, ?, ?, ?, ?, ?, ?);',
            u_id)
        connect.commit()
    else:
        print('Пользователь уже существует')


def read_user_info_database(message):
    user_id = message.chat.id
    connect = sqlite3.connect('users.db')
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')
    row = cursor.fetchone()
    return row


# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет', reply_markup=first_level_keyboard(), parse_mode='HTML')
    create_database(message)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Профиль':
        bot.send_message(message.chat.id, 'Ваша статистика: ')
        data = read_user_info_database(message)
        # check-data-info
        print(data)
        bot.send_message(message.chat.id,
                         f'id: {data[0]}\nusername: {data[1]}\nИмя пользователя: {data[2]}\nФамилия: {data[3]}\n\nПройденные курсы:\nPython 1 lvl: {data[4]}\nPython 2 lvl: {data[5]}\nC++ 1 lvl: {data[6]}\nC++ 2 lvl: {data[7]}')
    elif message.text == "С++":
        bot.send_message(message.chat.id, "Вы выбрали С++")
    elif message.text == "Javascript":
        bot.send_message(message.chat.id, "Вы выбрали Javascript")
    elif message.text == "Python":
        bot.send_message(message.chat.id, "Вы выбрали Python")
    else :
        bot.send_message(message.chat.id, "Не известная команда")


bot.polling(none_stop=True)
