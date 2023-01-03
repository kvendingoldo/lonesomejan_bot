# -*- coding: utf-8 -*-

from contextlib import AbstractContextManager
from typing import Callable, Iterator, Mapping

from sqlalchemy.orm import Session

from utils import repo
from models.user import User
from db.exceptions import UserNotFoundError


class UserRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def add(self, user: User) -> User:
        with self.session_factory() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    def get_by_id(self, id: str) -> User:
        with self.session_factory() as session:
            user = session.query(User).filter(User.id == id).first()
            if not user:
                raise UserNotFoundError(id)
            return user
