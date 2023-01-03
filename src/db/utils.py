# -*- coding: utf-8 -*-

from db import database
from db.repo.user import UserRepository

from db.repo.meet import MeetRepository


def get_repos(config):
    db = database.Database(config["database"]["url"])
    db.create_database()

    user_repo = UserRepository(session_factory=db.session)
    meet_repo = MeetRepository(session_factory=db.session)

    return user_repo, meet_repo
