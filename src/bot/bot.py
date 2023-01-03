# -*- coding: utf-8 -*-

import telebot
import json
import sys
import logging
import time

from utils import config as cfg_utils
from db import utils as db_utils
from telebot import TeleBot, types
from models import user

sys.path.append('../resources/')

bot = TeleBot("")
telebot.logger.setLevel(logging.INFO)

# bot.enable_save_next_step_handlers(delay=2)

config = cfg_utils.load("../resources/config.yml")
user_repo, meet_repo = db_utils.get_repos(config)

text_messages = {
    'start':
        u'Приветствую, {name}! Выбери необходимое действие в меню ✨'
}


@bot.message_handler(commands=['start'])
def start(message):
    print('KK')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    username = message.from_user.username
    if username == "kvendingoldo":
        markup.row('показать пары', 'показать игроков')
    else:
        markup.row('проверить заявку', 'подать заявку', 'отменить заявку')

    msg = bot.send_message(message.from_user.id,
                           text_messages['start'].format(name=message.from_user.first_name),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, handler)


@bot.message_handler(content_types=['text'])
def handler(message):
    # print(message)
    # db = connect(db_url, db_collection)
    # new_menu = []
    # new_msg = ''
    # new_handler = None

    if message.text == 'показать пары':
        msg = bot.send_message(message.from_user.id, "tst")
    elif message.text == 'показать игроков':
        msg = bot.send_message(message.from_user.id, "tst")

    elif message.text == 'подать заявку':
        try:
            usr2 = user_repo.get_by_id(id=message.from_user.id)
            if usr2.had_pair:
                msg = bot.send_message(message.from_user.id, "Вы уже подали заявку")
            else:
                msg = bot.send_message(message.from_user.id, "tst")
        except Exception as e:
            print(e)


        try:
            user_repo.add(user.User(
                id=message.from_user.id,
                username=message.from_user.username,
                first_name=message.from_user.first_name,
                last_name=message.from_user.last_name,
                has_pair=0
            ))
        except Exception as e:
            print(e)
        msg = bot.send_message(message.from_user.id, "tst")
    elif message.text == 'проверить заявку':
        try:
            usr = user_repo.get_by_id(id=message.from_user.id)
            if usr.has_pair:
                meet = meet_repo.list(spec={"or": {"uid1": usr.id, "uid2": usr.id}})[0]

                uid2 = ""
                if meet.uid1 == usr.id:
                    uid2 = meet.uid1
                else:
                    uid2 = meet.uid2


                usr2 = user_repo.get_by_id(id=uid2)
                msg = bot.send_message(message.from_user.id, "Ваша пара - %s" % usr2.username)

            else:
                msg = bot.send_message(message.from_user.id, "Мы все еще ищем вам пару 🥲 Как только найдет, но пришлем сообщение.")

        except Exception as e:
            print(e)




    elif message.text == 'отменить заявку':
        msg = bot.send_message(message.from_user.id, "tst")
    else:
        msg = bot.send_message(message.from_user.id,
                               "Похоже, что вы введи что-то не то; Попробуйте начать заного с помощью команды /start")

    # markup = create_menu(new_menu, back=True)
    msg = bot.send_message(message.from_user.id, new_msg, reply_markup=markup)
    # bot.register_next_step_handler(msg, new_handler)


def run():
    while True:
        try:
            bot.polling(non_stop=True, interval=1, timeout=10)
        except Exception as e:
            logging.info("[telegram] Failed: %s" % e)
            time.sleep(15)
