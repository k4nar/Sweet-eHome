from mongokit import Document

class Action(Document):

    use_dot_notation = True

    structure = {
        'name': basestring,
        'description': basestring,
        'args': {},
    }

    required_flags = ['name']