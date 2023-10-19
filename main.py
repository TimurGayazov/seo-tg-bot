import telebot
import sqlite3
from PIL import Image, ImageDraw, ImageFont
from telebot import types
bot = telebot.TeleBot('6630395700:AAEPNADLVlfc7HvH01pPDWJ81w5vAP4TNQw')
print('The server is running')

db_name = 'database.db'
flvl_keyboard_names = ["Python 1️⃣", "С++ 1️⃣", "Javascript 1️⃣", "👾 Профиль", "Python 2️⃣", "С++ 2️⃣", "Javascript 2️⃣"]

def first_level_keyboard():
    keyboard = telebot.types.ReplyKeyboardMarkup(True, False)
    keyboard.row(flvl_keyboard_names[0], flvl_keyboard_names[1], flvl_keyboard_names[2])
    keyboard.row(flvl_keyboard_names[4], flvl_keyboard_names[5], flvl_keyboard_names[6])
    keyboard.add(flvl_keyboard_names[3])
    return keyboard


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
    keyboard.add('Начать заново')
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
            python_first_test INTEGER,
            python_second_test INTEGER,
            c_first_test INTEGER,
            c_second_test INTEGER,
            js_first_test INTEGER,
            js_second_test INTEGER
        )""")
    connect.commit()

    u_chat_id = message.chat.id
    cursor.execute(f'SELECT id FROM users WHERE id = {u_chat_id}')
    data = cursor.fetchone()
    if data is None:
        u_id = [message.chat.id, message.from_user.username, message.from_user.first_name, message.from_user.last_name, 0, 0, 0, 0, 0, 0]
        cursor.execute(
            'INSERT INTO users (id, username, first_name, last_name, python_first_test, python_second_test, c_first_test, c_second_test, js_first_test, js_second_test) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);',
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


def read_test_info_se():
    table_name = "python1"
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    return rows


def write_test_score_user_database():
    pass

def create_sert(message):

    table_name = "users"
    connect = sqlite3.connect(db_name)
    cursor = connect.cursor()
    cursor.execute(f'SELECT * FROM {table_name}')
    rows = cursor.fetchall()
    full_name = ""
    full_name = str(message.from_user.last_name) + " " + str(message.from_user.first_name)
    image = Image.open("sert.jpg")

    draw = ImageDraw.Draw(image)

    font = ImageFont.truetype("arial.ttf", 20)

    draw.text((150, 360), full_name, font=font, fill="black")
    draw.text((920, 440), "5", font=font, fill="black")

    image.save(f"users_serts/{message.chat.id}.jpg")

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет', reply_markup=first_level_keyboard(), parse_mode='HTML')
    create_database(message)


@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == flvl_keyboard_names[3]:
        bot.send_message(message.chat.id, 'Ваша статистика: ')
        data = read_user_info_database(message)
        # check-data-info
        print(data)
        bot.send_message(message.chat.id,
                         f'id: {data[0]}\nusername: {data[1]}\nИмя: {data[2]}\nФамилия: {data[3]}\n\nРезультаты тестов:\nPython 1 lvl: {data[4]}\nPython 2 lvl: {data[5]}\nC++ 1 lvl: {data[6]}\nC++ 2 lvl: {data[7]}\nJavaScript 1 lvl: {data[8]}\nJavaSrcipt 2 lvl: {data[9]}')
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
        table_name = 'python1'
        bot.send_message(message.chat.id, "Для того чтобы начать тест 'Python 1 lvl' нажмите 'Начать' ", reply_markup=second_level_keyboard())
        bot.register_next_step_handler(message, test_func)
    elif message.text == flvl_keyboard_names[1]:
        bot.send_message(message.chat.id, "Вы выбрали C++")
    elif message.text == flvl_keyboard_names[2]:
        bot.send_message(message.chat.id, "Вы выбрали Javascript")

    elif message.text == flvl_keyboard_names[4]:
        bot.send_message(message.chat.id, "Вы выбрали Python")
    elif message.text == flvl_keyboard_names[5]:
        bot.send_message(message.chat.id, "Вы выбрали C++")
    elif message.text == flvl_keyboard_names[6]:
        bot.send_message(message.chat.id, "Вы выбрали Javascript")
    else:
        bot.send_message(message.chat.id, "Не известная команда")


def test_func(message, current_question=0, score=0):
    data = read_test_info_se()
    arr = data[current_question][2].split(",")
    string = ""
    for i in range (0, len(arr)):
        string += str(i + 1) + ") " + arr[i] + "\n"
    if current_question < len(data):
        bot.send_message(message.chat.id, "Выберите правильный ответ: ", reply_markup=third_level_keyboard())
        bot.send_message(message.chat.id, f'Вопрос #{data[current_question][0]}\n\n{data[current_question][1]}'
                                          f'\nВарианты ответов:\n{string}\n\nПравильный ответ: {data[current_question][3]}')
        bot.register_next_step_handler(message, check_answer, current_question, data, score)
    else:
        bot.send_message(message.chat.id, f'Тестирование окончено!\nВаш результат: {score}', reply_markup=first_level_keyboard())



def check_answer(message, current_question, data, score):
    if message.text == data[current_question][3]:
        bot.send_message(message.chat.id, "Ответ принят.")
        score += 1
    else:
        bot.send_message(message.chat.id, "Ответ не принят.")

    current_question += 1
    test_func(message, current_question, score)


bot.polling(none_stop=True)
