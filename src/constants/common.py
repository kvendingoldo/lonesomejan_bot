# -*- coding: utf-8 -*-

from pydantic.dataclasses import dataclass



@dataclass
class DBTables:
    user: str = 'user'
    meet: str = 'meet'



DB_TABLES = DBTables()
