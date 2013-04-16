from mongokit import Document

from connection import connection, db

from action import Action

devices = db.devices

@connection.register
class Device(Document):
    """A device stored in Mongodb"""

    use_dot_notation = True

    __database__ = 'sweet-ehome'
    __collection__ = 'devices'

    structure = {
        '_last_updated': int,

        'id': basestring,
        'driver': basestring,
        'connected': bool,
        'actions': [Action],
        'params': dict,
        'infos': dict,
    }

    indexes = [
        {
            'fields': ['id'],
            'unique': True,
        },
        {
            'fields': ['driver', '_last_updated']
        }
    ]

    required_fields = ['id', 'driver']

    default_values = {'connected': False}

    @staticmethod
    def all_to_api(query=None):
        return [d.apize(shorten=True) for d in devices.Device.fetch(query)]

    @staticmethod
    def to_api(id):
        device = Device.by_id(id)
        if device:
            return device.apize()
        return None

    @staticmethod
    def by_id(id):
        return devices.Device.fetch_one({"id": id})

    @staticmethod
    def get_updated_since(timestamp):
        updated = []
        for device in devices.Device.fetch({"_last_updated": {"$gt": timestamp}}):
            d = device.apize()
            d.pop("actions")
            updated.append(d)
        return updated

    def url(self):
        return "/devices/{}".format(self.id)

    def apize(self, shorten=False, actions=True):
        out = dict(self)
        out.pop("_id")
        out.pop("_last_updated")

        out["url"] = self.url()
        if actions:
            if shorten:
                out["actions"] = "{}/actions".format(out["url"])
            else:
                out["actions"] = self.all_actions()

        if shorten:
            for e in ["params", "infos"]:
                out[e] = "{}/{}".format(out["url"], e)

        return out

    def all_actions(self):
        def _apize_action(action):
            action.pop("_id")
            return action

        return [_apize_action(a) for a in self.actions if a]

def disconnect_all():
    for device in devices.Device.fetch():
        device.connected = False
        device.save()
