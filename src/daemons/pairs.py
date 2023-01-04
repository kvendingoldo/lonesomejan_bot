# -*- coding: utf-8 -*-

import time
import random
import telebot

import logging

from db import utils as db_utils


def run(config):
    logging.info("Hello from create pair thread")

    user_repo = db_utils.get_repos(config)
    bot = telebot.TeleBot(config["telegram"]["token"])
    telebot.logger.setLevel(logging.INFO)

    while True:
        users = user_repo.list()
        for usr in users:
            if usr.pair != "none" :
                users.remove(usr)

        random.shuffle(users)

        while len(users) > 1:
            usr1 = users[0]
            usr2 = users[1]

            usr1.pair = usr2.id
            usr2.pair = usr1.id

            user_repo.update(usr1)
            user_repo.update(usr2)

            users.remove(usr1)
            users.remove(usr2)

            try:
                bot.send_message(
                    usr1.id, 'Привет, %s 👋 Мы нашли для тебя пару, это @%s.'
                                 % (usr1.first_name, usr2.username)
                )
            except Exception as ex:
                print(ex)

            bot.send_message(
                usr2.id, 'Привет, %s 👋 Мы нашли для тебя пару, это @%s.'
                             % (usr2.first_name, usr1.username)
            )

        time.sleep(config["daemons"]["pairs"]["period"])
