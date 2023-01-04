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

    def delete_by_id(self, id: str) -> None:
        with self.session_factory() as session:
            entity: User = session.query(User).filter(User.id == id).first()
            if not entity:
                raise UserNotFoundError(id)
            session.delete(entity)
            session.commit()

    def list(self, spec: Mapping = None) -> Iterator[User]:
        with self.session_factory() as session:
            objs = session.query(User).all()

        return repo.filtration(spec, objs)

    def update(self, user: User) -> None:
        with self.session_factory() as session:
            session.query(User).filter_by(id=user.id).update(dict(
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                pair=user.pair
            ))

            session.commit()
