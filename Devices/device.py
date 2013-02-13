from mongokit import Document

from connection import Connection
from action import Action

class StoredDevice(Document):
    """A base device stored in Mongodb"""

    __database__ = 'sweet-ehome'
    __collection__ = 'devices'

    structure = {
        'type': basestring,
        'actions': [Action()],
        'params': dict,
        'connection': Connection(),
    }

    required_fields = ['type', 'actions', 'infos', 'connection']
