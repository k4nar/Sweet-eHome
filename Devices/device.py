from mongokit import Document, Connection

from action import Action


connection = Connection()
devices = connection["sweet-ehome"].devices

@connection.register
class StoredDevice(Document):
    """A base device stored in Mongodb"""

    __database__ = 'sweet-ehome'
    __collection__ = 'devices'

    structure = {
        'id': basestring,

        'driver': basestring,

        'type': basestring,

        'actions': [Action()],
        'params': dict,
    }

    required_fields = ['id', 'driver', 'type']
