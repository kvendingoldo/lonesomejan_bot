# -*- coding: utf-8 -*-

class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found, id: {entity_id}')


class MeetNotFoundError(NotFoundError):
    entity_name: str = 'Meet'




class UserNotFoundError(NotFoundError):
    entity_name: str = 'User'
