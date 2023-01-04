# -*- coding: utf-8 -*-

import prettytable as pt
import telebot
import sys
import logging
import time

from utils import config as cfg_utils
from db import utils as db_utils
from models import user
from db.exceptions import UserNotFoundError

sys.path.append('../resources/')
config = cfg_utils.load("../resources/config.yml")

bot = telebot.TeleBot(config["telegram"]["token"])
telebot.logger.setLevel(logging.INFO)

user_repo = db_utils.get_repos(config)

text_messages = {
    'start': u'{name}, привет! Выбери необходимое действие в меню ✨',
    'sr_found': 'Вы уже подали заявку; Ваш партнер %s',
    'sr_still_looking': u'Вы уже подали заявку 💪 Мы пока еще ищем вам партнера и сразу же пришем вам сообщение, как найдем',
    'sr_accepted': 'Мы приняли вашу заявку 🔥 Сразу же напишем вам сообщение, как найдем партнера',

    'cr_check': 'Ваша пара - @%s',
    'cr_still_looking': 'Мы все еще ищем вам пару 🥲 Как только найдет, но пришлем сообщение',
    'cr_cant_find_you': 'Мы не можем найти вашу заявку, попробуйте подать ее еще раз через форму подачи заявки',

    'ar_by_partner': 'Ваш партнер отменил заявку, мы постараемся найти вам новую пару',
    'ar_successfully': 'Ваша заявка отменена',

    'wrong_usr': 'Похоже, что вы введи что-то не то; Попробуйте начать заного с помощью команды /start',
    'wrong_srv': 'Похоже что-то пошло не так, попробуйте еще раз'
}


@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.row('проверить заявку', 'подать заявку', 'отменить заявку')
    if message.from_user.username == config["admin"]["username"]:
        markup.row('показать пары', 'показать игроков')

    msg = bot.send_message(message.from_user.id,
                           text_messages['start'].format(name=message.from_user.first_name),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, handler)


@bot.message_handler(content_types=['text'])
def handler(message):
    if message.text == 'показать пары':
        try:
            users = user_repo.list()

            id2name = []
            for usr in users:
                id2name.append({'id': usr.id, 'username': usr.username})

            table = pt.PrettyTable(['u1', 'u2'])

            while len(users) > 0:
                usr = users[0]
                uid2 = "none"

                for i2n in id2name:
                    if i2n["id"] == usr.pair:
                        uid2 = i2n["id"]
                        table.add_row([usr.username, i2n["username"]])
                        break

                users.remove(usr)
                for usr in users:
                    if usr.id == uid2:
                        users.remove(usr)
                        break
            msg = bot.send_message(message.from_user.id, f'```{table}```', parse_mode='MarkdownV2')
        except Exception as ex:
            msg = bot.send_message(message.from_user.id, text_messages["wrong_srv"])
            logging.error(ex)

    elif message.text == 'показать игроков':
        try:
            users = user_repo.list()
            table = pt.PrettyTable(['username', 'status'])

            for usr in users:
                if usr.pair != "none":
                    table.add_row((usr.username, "✅"))
                else:
                    table.add_row((usr.username, "❌"))
            msg = bot.send_message(message.from_user.id, f'```{table}```', parse_mode='MarkdownV2')
        except Exception as ex:
            msg = bot.send_message(message.from_user.id, text_messages["wrong_srv"])
            logging.error(ex)

    elif message.text == 'подать заявку':
        try:
            usr = user_repo.get_by_id(id=message.from_user.id)
            if usr.pair != "none":
                try:
                    usr2 = user_repo.get_by_id(id=usr.pair)
                    msg = bot.send_message(message.from_user.id, text_messages["sr_found"] % usr2.username)
                except Exception as ex:
                    msg = bot.send_message(message.from_user.id, text_messages["wrong_srv"])
                    logging.error(ex)
            else:
                msg = bot.send_message(message.from_user.id, text_messages["sr_still_looking"])
        except UserNotFoundError as ex:
            try:
                user_repo.add(user.User(
                    id=message.from_user.id,
                    username=message.from_user.username,
                    first_name=message.from_user.first_name,
                    last_name=message.from_user.last_name,
                    pair="none"
                ))
                msg = bot.send_message(message.from_user.id, text_messages["sr_accepted"])
            except Exception as ex:
                msg = bot.send_message(message.from_user.id, text_messages["wrong_srv"])
                logging.error(ex)

    elif message.text == 'проверить заявку':
        try:
            usr = user_repo.get_by_id(id=message.from_user.id)

            if usr.pair != "none":
                try:
                    usr = user_repo.get_by_id(id=usr.pair)
                    msg = bot.send_message(message.from_user.id, text_messages["cr_check"] % usr.username)
                except UserNotFoundError as ex:
                    msg = bot.send_message(message.from_user.id, text_messages["wrong_srv"])
                    logging.error(ex)
            else:
                msg = bot.send_message(message.from_user.id, text_messages["cr_still_looking"])
        except UserNotFoundError as ex:
            msg = bot.send_message(message.from_user.id, text_messages["cr_cant_find_you"])
            logging.error(ex)
        except Exception as ex:
            msg = bot.send_message(message.from_user.id, text_messages["wrong_srv"])
            logging.error(ex)

    elif message.text == 'отменить заявку':
        try:
            usr = user_repo.get_by_id(id=message.from_user.id)
            if usr.pair != "none":
                uid2 = usr.pair
                try:
                    user_repo.delete_by_id(uid2)
                    msg = bot.send_message(uid2, text_messages["ar_by_partner"])
                except Exception as ex:
                    msg = bot.send_message(message.from_user.id, text_messages["wrong_srv"])
                    logging.error(ex)

            try:
                user_repo.delete_by_id(usr.id)
                msg = bot.send_message(message.from_user.id, text_messages["ar_successfully"])
            except Exception as ex:
                msg = bot.send_message(message.from_user.id, text_messages["wrong_srv"])
                logging.error(ex)

        except UserNotFoundError as ex:
            msg = bot.send_message(message.from_user.id, text_messages["cant_find_request"])
            logging.error(ex)

    else:
        msg = bot.send_message(message.from_user.id, text_messages["wrong_usr"])


def run():
    while True:
        try:
            bot.polling(non_stop=True, interval=0, timeout=10)
        except Exception as ex:
            logging.info("[telegram] Failed: %s" % ex)
            time.sleep(3)
