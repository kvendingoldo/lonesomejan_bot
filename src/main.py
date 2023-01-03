# -*- coding: utf-8 -*-

import datetime
import logging
import time
import os

from threading import Thread

#from utils.parser import prepare_basic_collections
#from utils.updater import update_scenes_daemon, update_authors_daemon
from bot.bot import run
#from config import data_dir, first_run
from utils import config as cfg_utils

#LOG_DIR = '%s/log' % data_dir

if __name__ == '__main__':
    config = cfg_utils.load("../resources/config.yml")

    #os.makedirs(LOG_DIR, exist_ok=True)
    #log_name = '%s/%s.log' % (LOG_DIR, datetime.datetime.now().strftime('%d_%m_%Y_%H_%M'))
    #logging.basicConfig(filename=log_name, level=logging.DEBUG)



    # update_authors_proccess = Thread(target=update_scenes_daemon, args=())
    # update_authors_proccess.start()
    #
    # update_authors_proccess = Thread(target=update_authors_daemon, args=())
    # update_authors_proccess.start()
    #
    #
    #
    print("abc")
    telegram_bot_proccess = Thread(target=run, args=())
    telegram_bot_proccess.start()
