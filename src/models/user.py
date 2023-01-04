# -*- coding: utf-8 -*-

from sqlalchemy import Column, String, DateTime
from sqlalchemy.sql import func

from db.database import Base
from constants import common


class User(Base):
    __tablename__ = common.DB_TABLES.user

    id = Column(String(48), primary_key=True, nullable=False, unique=True)
    username = Column(String(92), nullable=False, unique=False)
    first_name = Column(String(24), nullable=False, unique=False, default="none")
    last_name = Column(String(24), nullable=False, unique=False, default="none")

    pair = Column(String(48), nullable=False, unique=False, default="none")

    tmst_created = Column(DateTime(timezone=True), server_default=func.now())
    tmst_updated = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f'<User(id="{self.id}", ' \
               f'username="{self.username}", ' \
               f'fist_name="{self.first_name}", ' \
               f'last_name="{self.last_name}")>' \
               f'pair="{self.pair}")>'
