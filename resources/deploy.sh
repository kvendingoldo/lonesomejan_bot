#!/bin/bash

VERSION="VERSION"
TBOT_TOKEN="TOKEN"

docker run -d \
    -v /home/ubuntu/tbot/lonesomejan.db:/home/tbot/bot/lonesomejan.db \
    -e LOG_DIR="" \
    -e DB_URL=sqlite:////home/tbot/bot/lonesomejan.db \
    -e TG_BOT_TOKEN=${TBOT_TOKEN} \
    kvendingoldo/lonesomejan_bot:${VERSION}
