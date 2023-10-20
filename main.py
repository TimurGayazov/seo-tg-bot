import telebot
import sqlite3
import os
from PIL import Image, ImageDraw, ImageFont
from telebot import types
bot = telebot.TeleBot('6630395700:AAEPNADLVlfc7HvH01pPDWJ81w5vAP4TNQw')
print('The server is running')

db_name = 'database.db'
flvl_keyboard_names = ["Python 1️⃣", "С++ 1️⃣", "JavaScript 1️⃣", "👾 Профиль", "Python 2️⃣", "С++ 2️⃣", "JavaScript 2️⃣"]


def first_level_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row(flvl_keyboard_names[0], flvl_keyboard_names[1], flvl_keyboard_names[2])
    keyboard.row(flvl_keyboard_names[4], flvl_keyboard_names[5], flvl_keyboard_names[6])
    keyboard.add(flvl_keyboard_names[3])
    return keyboard


markup = types.InlineKeyboardMarkup()
button1 = types.InlineKeyboardButton("📜 Сертификаты 📜", callback_data='sert')
markup.add(button1)


@bot.callback_query_handler(func=lambda call: True)
def handle_callback(callback_query):
    if callback_query.data == 'sert':
        bot.send_message(callback_query.message.chat.id, "Ваши сертификаты")
        directory_path = 'users_serts'
        word_to_search = str(callback_query.message.chat.id)
        matching_files = [file for file in os.listdir(directory_path) if word_to_search in file]
        for file in matching_files:
            with open(f'users_serts/{file}', 'rb') as photo:
                bot.send_photo(callback_query.message.chat.id, photo)
            print(file)


def read_table():
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    rows = cursor.fetchall()
    return rows


def second_level_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.add('Начать')
    keyboard.add('Назад')
    return keyboard


def third_level_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row('1', '2')
    keyboard.row('3', '4')
    return keyboard


# database
def create_database(message):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
            id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            python1 INTEGER,
            python2 INTEGER,
            c1 INTEGER,
            c2 INTEGER,
            js1 INTEGER,
            js2 INTEGER
        )""")
    connect.commit()

    u_chat_id = message.chat.id
    cursor.execute(f'SELECT id FROM users WHERE id = {u_chat_id}')
    data = cursor.fetchone()
    if data is None:
        u_id = [message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, 0, 0, 0, 0, 0, 0]
        cursor.execute(
            'INSERT INTO users (id, username, first_name, last_name, python1, python2, c1, c2, js1, js2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
            u_id)
        connect.commit()
    else:
        print('Пользователь уже существует')


def read_user_info_database(message):
    user_id = message.chat.id
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM users WHERE id = {user_id}')
    row = cursor.fetchone()
    return row


def create_database_test(message):
    message_list = message.text.split(' ')
    table_name = message_list[1]
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f"""CREATE TABLE IF NOT EXISTS {table_name}(
                id_question INTEGER,
                question TEXT,
                answers TEXT,
                right_answer TEXT
            )""")
    connect.commit()
    count_question = int(input('Введите количесвто вопросов: '))
    for i in range(0, count_question):
        id_question = i+1
        question_name = input(f'Введите вопрос номер {id_question}: ')
        answer_options = input(f'Введите варианты ответов через ,: ')
        right_answer = input('Введите правильный ответ от 1 до 4: ')
        table_data = [id_question, question_name, answer_options, right_answer]
        cursor.execute(
            f'INSERT INTO {table_name} (id_question, question, answers, right_answer) VALUES (?, ?, ?, ?);', table_data)
        connect.commit()


def delete_database_test(message):
    message_list = message.text.split(' ')
    table_name = message_list[1]
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    connect.commit()


def read_test_info(message):
    message_list = message.text.split(' ')
    table_name = message_list[1]
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    return rows


def read_test_info_se(table_name):
    # table_name = "python1"
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    return rows


def write_test_score_user_database(message, score, table_name):
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    new_value = score
    update_query = f"UPDATE users SET {table_name} = {new_value} WHERE id = {message.chat.id}"
    cursor.execute(update_query)
    connect.commit()


def create_sert(message, table_name):
    user_id = message.chat.id
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f'SELECT {table_name} FROM users WHERE id = {user_id}')
    row = cursor.fetchone()
    if int(*row) >= 8:
        full_name = ""
        full_name = str(message.from_user.last_name) + " " + str(message.from_user.first_name)
        image = Image.open("sert.jpg")
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 20)
        score = int(*row) *10
        test_name = ''
        if table_name == 'python1':
            test_name = 'Python 1 lvl'
        elif table_name == 'python2':
            test_name = 'Python 2 lvl'
        elif table_name == 'c1':
            test_name = 'C++ 1 lvl'
        elif table_name == 'c2':
            test_name = 'C++ 2 lvl'
        elif table_name == 'js1':
            test_name = 'JavaScript 1 lvl'
        elif table_name == 'js2':
            test_name = 'JavaScript 2 lvl'

        draw.text((150, 360), full_name, font=font, fill="black")
        draw.text((150, 440), test_name, font=font, fill="black")
        draw.text((920, 440), f'{score}%', font=font, fill="black")
        sert_name = ''
        sert_name = str(message.chat.id) + ' ' + str(table_name)
        image.save(f"users_serts/{sert_name}.jpg")


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Приветствую тебя', reply_markup=first_level_keyboard(), parse_mode='HTML')
    bot.send_message(message.chat.id, '👋', reply_markup=first_level_keyboard(), parse_mode='HTML')
    bot.send_message(message.chat.id, 'Для того чтобы пройти тестирование выбери тест на клавиатуре ⬇️', reply_markup=first_level_keyboard(), parse_mode='HTML')
    create_database(message)


table_name = None


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == flvl_keyboard_names[3]:
        bot.send_message(message.chat.id, '👾 Ваш профиль 👾')
        data = read_user_info_database(message)
        # check-data-info
        print(data)
        bot.send_message(message.chat.id,
                         f'id: {data[0]}\nusername: {data[1]}\nИмя: {data[2]}\nФамилия: {data[3]}\n\nРезультаты тестов:\nPython 1 lvl: {data[4]*10}%\nPython 2 lvl: {data[5]*10}%\nC++ 1 lvl: {data[6]*10}%\nC++ 2 lvl: {data[7]*10}%\nJavaScript 1 lvl: {data[8]*10}%\nJavaSrcipt 2 lvl: {data[9]*10}%', reply_markup=markup)
    elif '/createtest' in message.text:
        create_database_test(message)
        bot.send_message(message.chat.id, "Тест успешно создан!")

    elif '/deletetest' in message.text:
        delete_database_test(message)
        bot.send_message(message.chat.id, "Тест успешно удален!")

    elif '/readtable' in message.text:
        data = read_table()
        print(*data[1])

    elif '/image' in message.text:
        with open('sert.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
        create_sert(message)

    elif '/testcommand' in message.text:
        data = read_test_info(message)
        print(data)
        for i in range(0, len(data)):
            bot.send_message(message.chat.id, f'Вопрос #{data[i][0]}\n\n{data[i][1]}\nВарианты ответов: {data[i][2]}\n\nПравильный ответ: {data[i][3]}')

    elif '/testfunc' in message.text:
        bot.send_message(message.chat.id, "Для того чтобы начать тестирование нажмите 'Начать' ", reply_markup=second_level_keyboard())
        bot.register_next_step_handler(message, test_func)

    elif message.text == flvl_keyboard_names[0]:
        global table_name
        table_name = 'python1'
        bot.send_message(message.chat.id, "Для того чтобы начать тест 'Python 1 lvl' нажмите 'Начать' ", reply_markup=second_level_keyboard())
        bot.register_next_step_handler(message, test_func)

    elif message.text == flvl_keyboard_names[1]:
        table_name = 'c1'
        bot.send_message(message.chat.id, "Для того чтобы начать тест 'C++ 1 lvl' нажмите 'Начать' ",
                         reply_markup=second_level_keyboard())
        bot.register_next_step_handler(message, test_func)

    elif message.text == flvl_keyboard_names[2]:
        table_name = 'js1'
        bot.send_message(message.chat.id, "Для того чтобы начать тест 'JavaScript 1 lvl' нажмите 'Начать' ",
                         reply_markup=second_level_keyboard())
        bot.register_next_step_handler(message, test_func)

    elif message.text == flvl_keyboard_names[4]:
        table_name = 'python2'
        bot.send_message(message.chat.id, "Для того чтобы начать тест 'Python 2 lvl' нажмите 'Начать' ",
                         reply_markup=second_level_keyboard())
        bot.register_next_step_handler(message, test_func)

    elif message.text == flvl_keyboard_names[5]:
        table_name = 'c2'
        bot.send_message(message.chat.id, "Для того чтобы начать тест 'C++ 2 lvl' нажмите 'Начать' ",
                         reply_markup=second_level_keyboard())
        bot.register_next_step_handler(message, test_func)

    elif message.text == flvl_keyboard_names[6]:
        table_name = 'js2'
        bot.send_message(message.chat.id, "Для того чтобы начать тест 'JavaScript 2 lvl' нажмите 'Начать' ",
                         reply_markup=second_level_keyboard())
        bot.register_next_step_handler(message, test_func)
    else:
        bot.send_message(message.chat.id, "Не известная команда")


def test_func(message, current_question=0, score=0):
    if message.text == 'Назад':
        bot.send_message(message.chat.id, "Вы вернулись в главное меню.", reply_markup=first_level_keyboard())
    else:
        data = read_test_info_se(table_name)
        if current_question < len(data):
            arr = data[current_question][2].split(",")
            string = ""
            for i in range(0, len(arr)):
                string += str(i + 1) + ") " + arr[i] + "\n"
            bot.send_message(message.chat.id, "Выберите правильный ответ: ⬇️", reply_markup=third_level_keyboard())
            bot.send_message(message.chat.id, f'Вопрос #{data[current_question][0]}\n\n{data[current_question][1]}'
                                              f'\nВарианты ответов:\n{string}\n\nПравильный ответ: {data[current_question][3]}')
            bot.register_next_step_handler(message, check_answer, current_question, data, score)
        else:
            final_score = score * 10
            bot.send_message(message.chat.id, f'Тестирование окончено!\nВаш результат: {final_score}%',
                             reply_markup=first_level_keyboard())
            if score >= 8:
                bot.send_message(message.chat.id, "🔥", reply_markup=first_level_keyboard())
                bot.send_message(message.chat.id, "Вы успешно прошли тест!\nСертификат доступен в вашем профиле.",
                                 reply_markup=first_level_keyboard())
            else:
                bot.send_message(message.chat.id,
                                 "К сожалению вы не прошли тест\nДля получения сертификата нужно набрать не менее 80%\nПопробуйте пройти еще раз.",
                                 reply_markup=first_level_keyboard())

            write_test_score_user_database(message, score, table_name)
            create_sert(message, table_name)



def check_answer(message, current_question, data, score):
    if message.text == data[current_question][3]:
        bot.send_message(message.chat.id, "✅")
        score += 1
    else:
        bot.send_message(message.chat.id, "❌")

    current_question += 1
    test_func(message, current_question, score)


bot.polling(none_stop=True)
