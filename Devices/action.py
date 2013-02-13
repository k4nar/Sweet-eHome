from mongokit import Document

class Action(Document):

    structure = {
        'name': basestring,
        'description': basestring,
        'args': {},
    }

    required_flags = ['name']