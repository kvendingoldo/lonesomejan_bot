# -*- coding: utf-8 -*-

import os
import yaml


def load(yaml_path):
    with open(yaml_path, "r") as file:
        config = yaml.safe_load(file)

#    slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
#    slack_app_token = os.environ["SLACK_APP_TOKEN"]

    #db_password = os.environ.get("DATABASE_PASSWORD")

    # config["slack"] = {
    #     "botToken": slack_bot_token,
    #     "appToken": slack_app_token
    # }

    #config["database"]["password"] = db_password

    return config