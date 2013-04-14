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
        'id': basestring,
        'driver': basestring,
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
            'fields': ['driver']
        }
    ]

    required_fields = ['id', 'driver']

    @staticmethod
    def all():
        return [d.apize(shorten=True) for d in devices.Device.fetch()]

    @staticmethod
    def by_id(id):
        device = devices.Device.fetch_one({"id": id})
        if device:
            return device.apize()
        return None

    def url(self):
        return "/devices/{}".format(self.id)

    def apize(self, shorten=False):
        out = dict(self)
        out.pop("_id")

        out["url"] = self.url()
        out["actions"] = self.all_actions()

        if shorten:
            for e in ["actions", "params", "infos"]:
                out[e] = "{}/{}".format(out["url"], e)

        return out

    def all_actions(self):
        def _apize_action(action):
            action.pop("_id")
            return action

        return [_apize_action(a) for a in self.actions if a]
