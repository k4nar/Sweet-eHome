from mongokit import Document

from connection import connection, db

actions = db.actions

@connection.register
class Action(Document):

    use_dot_notation = True

    __database__ = 'sweet-ehome'
    __collection__ = 'actions'

    structure = {
        'name': basestring,
        'description': basestring,
        'args': [basestring],
    }

    indexes = [
        {
            'fields': ['name'],
            'unique': True,
        },
    ]

    required_flags = ['name']

    @staticmethod
    def all():
        return [a.apize(shorten=True) for a in actions.Action.fetch()]

    @staticmethod
    def by_name(name):
        action = actions.Action.fetch_one({"name": name})
        if action:
            return action.apize()
        return None

    def devices(self):
        return [{"url": device.url()} for device in db.devices.Device.fetch({"actions": {"$elemMatch": {'_id': self._id}}})]

    def url(self):
        return "/actions/{}".format(self.name)

    def apize(self, shorten=False):
        out = dict(self)

        out.pop("_id")

        out["url"] = self.url()

        if not shorten:
            out["devices"] = self.devices()

        return out

# All the known actions
defined_actions = [
    {
        "name": "on",
        "description": "Turns on a device",
        "args": [],
    },
    {
        "name": "off",
        "description": "Turns off a device",
        "args": [],
    },
    {
        "name": "toggle",
        "description": "Toggles the on/off status of a device",
        "args": [],
    },
    {
        "name": "variate",
        "description": "Change the variation of a device with a dimmer",
        "args": ["var"],
    },
]

def init_actions():
    for action in defined_actions:
        if not Action.by_name(action["name"]):
            a = actions.Action()
            for k, v in action.items():
                a[k] = v
            a.save()
