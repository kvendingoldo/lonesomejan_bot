# -*- coding: utf-8 -*-

from pydantic.dataclasses import dataclass


@dataclass
class DBTables:
    user: str = 'user'


DB_TABLES = DBTables()
