import random
import os
import telebot
import config
from telebot import types
from sqLighter import SQLither

koeff = 0.01
cur_id1 = 1
cur_id2 = 2
cur_rating1 = 0
cur_rating2 = 0

bot = telebot.TeleBot(config.token)

chats = {}


def create_markup(names):
    markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    for i in names:
        markup1.add(types.KeyboardButton(i))
    return markup1


def new_round(message):
    sql = SQLither("models.db")
    markup = create_markup(['/1', '/2'])
    max_len = sql.count_rows()
    a = random.randint(1, max_len)
    b = random.randint(1, max_len - 1)
    if b >= a:
        b += 1
    cur_id1 = a
    cur_id2 = b
    cur_rating1 = sql.select_single(a)[0][1]
    cur_rating2 = sql.select_single(b)[0][1]
    global chats
    chats[message.chat.id] = tuple([cur_id1, cur_id2, cur_rating1, cur_rating2])
    bot.send_photo(message.chat.id, open(str('pictures/' + str(a) + '.jpg'), 'rb'))
    bot.send_photo(message.chat.id, open(str('pictures/' + str(b) + '.jpg'), 'rb'), reply_markup=markup)
    sql.close()


def change_rating(id_a, id_b, wa, wb, ra, rb):
    sql = SQLither("models.db")
    delta = koeff * (wa * rb - wb * ra)
    sql.edit_rating(id_a, ra, delta)
    sql.edit_rating(id_b, rb, -delta)
    sql.close()


@bot.message_handler(commands=['help'])
def helper(message):
    bot.send_message(message.chat.id, "/help  - выводит список комманд \n"
                                      "/top5 - присылает фото топ 5 \n "
                                      "без '/' отправить номер, чтобы узнать кто скрывается под ним \n"
                                      "/new - новая битва титанов \n"
                                      "/rating - выводит упорядоченный список бойцов с номером и рейтингом\n")


@bot.message_handler(commands=['rating'])
def rat(message):
    sql = SQLither("models.db")
    rating = sql.select_all()
    rating.sort(key=lambda x: -x[1])
    ans = ""
    for i in range(len(rating)):
        ans += f'rank: {i + 1} {" " * (7 - len(str(i + 1)))} id:{rating[i][0]} {" " * (7 - len(str(rating[i][0])))} rating: {round(rating[i][1], 2)}\n'
    bot.send_message(message.chat.id, ans)
    sql.close()


@bot.message_handler(commands=['top5'])
def toppper(message):
    sql = SQLither("models.db")
    rating = sql.select_all()
    rating.sort(key=lambda x: -x[1])
    bot.send_photo(message.chat.id, open(str(f'pictures/{rating[0][0]}.jpg'), 'rb'))
    bot.send_photo(message.chat.id, open(str(f'pictures/{rating[1][0]}.jpg'), 'rb'))
    bot.send_photo(message.chat.id, open(str(f'pictures/{rating[2][0]}.jpg'), 'rb'))
    bot.send_photo(message.chat.id, open(str(f'pictures/{rating[3][0]}.jpg'), 'rb'))
    bot.send_photo(message.chat.id, open(str(f'pictures/{rating[4][0]}.jpg'), 'rb'))
    sql.close()


@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    sql = SQLither("models.db")

    try:

        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        current_file = os.path.realpath(__file__)
        current_directory = os.path.dirname(current_file)
        src = current_directory + '/pictures/' + file_info.file_path.replace('photos/', '');
        print(src)
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        os.rename(src, current_directory + '/pictures/' + str(sql.count_rows() + 1) + '.jpg')
        sql.add_new('-')
        bot.reply_to(message, "Фото добавлено")

    except Exception as e:
        bot.reply_to(message, e)
    sql.close()


@bot.message_handler(commands=['start'])
def starter(message):
    bot.send_message(message.chat.id, 'Добро пожаловать в бойцовский клуб!\n')
    helper(message)


@bot.message_handler(commands=['1'])
def continuer1(message):
    global chats
    if (chats.get(message.chat.id)):
        a = chats[message.chat.id]
        # print(a)
        change_rating(a[0], a[1], 1, 0, a[2], a[3])
    new_round(message)


@bot.message_handler(commands=['2'])
def continuer2(message):
    global chats
    if (chats.get(message.chat.id)):
        a = chats[message.chat.id]
        # print(a)
        change_rating(a[0], a[1], 0, 1, a[2], a[3])
    new_round(message)


@bot.message_handler(commands=['new'])
def newer(message):
    new_round(message)


@bot.message_handler(content_types=['text'])
def send_num(message):
    if message.text.isdigit():
        sql = SQLither("models.db")
        try:
            bot.send_photo(message.chat.id, open(f'pictures/{message.text}.jpg', 'rb'))
        except():
            bot.send_message(message.chat.id, "Увы, такого номера нет(")
        sql.close()


bot.infinity_polling()
