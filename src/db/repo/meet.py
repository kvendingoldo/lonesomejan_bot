# -*- coding: utf-8 -*-

import random

from contextlib import AbstractContextManager
from typing import Callable, Iterator, Mapping

from sqlalchemy.orm import Session, aliased
from utils import repo

from sqlalchemy import or_
from loguru import logger


from models.meet import Meet
from models.user import User
from db.exceptions import MeetNotFoundError


class MeetRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def create(self, uids, additional_uids=None, kind='random'):
        logger.info("Starting algorithm to create meets")

        if additional_uids is None:
            additional_uids = []
        if kind == 'random':
            self.__create_random(uids, additional_uids)

        logger.info("Algorithm for creating pairs has successfully completed")




    def add(self, meet: Meet) -> Meet:
        with self.session_factory() as session:
            session.add(meet)
            session.commit()
            session.refresh(meet)
            return meet

    def update(self, meet: Meet) -> None:
        with self.session_factory() as session:
            session.query(Meet).filter_by(id=meet.id).update(dict(
                season=meet.season,
                uid1=meet.uid1,
                uid2=meet.uid2,
                completed=meet.completed
            ))

            session.commit()

    def delete(self, meet: Meet) -> None:
        with self.session_factory() as session:
            entity: Meet = session.query(Meet).filter(Meet.id == meet.id).first()
            if not entity:
                raise MeetNotFoundError(meet.id)
            session.delete(entity)
            session.commit()

    def delete_all_by_uid(self, uid: str) -> None:
        with self.session_factory() as session:
            entities: Meet = session.query(Meet).filter(
                or_(Meet.uid1 == uid, Meet.uid2 == uid)
            )

            if not entities:
                raise MeetNotFoundError("")

            for entity in entities:
                session.delete(entity)

            session.commit()

    def list(self, spec: Mapping = None) -> list:
        with self.session_factory() as session:
            objs = session.query(Meet).all()

        return repo.filtration(spec, objs)

    def list_humanreadable(self) -> list:
        with self.session_factory() as session:
            u1 = aliased(User)
            u2 = aliased(User)

            objs = session.query(
                u1.username, u2.username, u1.meet_group, u2.meet_group, Meet.season, Meet.completed
            ).join(
                u1, u1.id == Meet.uid1
            ).join(
                u2, u2.id == Meet.uid2
            ).all()

        return objs
