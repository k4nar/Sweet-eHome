from mongokit import Document

class Connection(Document):

    structure = {
        'driver': basestring,
        'params': {},
    }

    required_fields = ['driver', 'params']
        