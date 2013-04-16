from time import time

from multiprocessing.managers import BaseManager

from Devices import devices, actions

class BaseDriver(object):
    """Base class for DomoLib drivers implementations"""

    name = "BaseDriver"

    def __init__(self):
        super(BaseDriver, self).__init__()

        self._core = None
        self._devices = devices
        self._actions = actions

    def _base_query(self):
        return {'driver': self.name}

    def _get_id(self, id):
        return "{}_{}".format(self.name, id)

    def devices(self, query=None):
        if query:
            query.update(self._base_query())
        else:
            query = self._base_query()

        return self._devices.Device.fetch(query)

    def device(self, id):
        query = {'id': self._get_id(id)}
        query.update(self._base_query())

        return self._devices.Device.fetch_one(query)

    def action(self, name):
        return self._actions.Action.fetch_one({"name": name})

    def new(self, id, attributes):
        id = self._get_id(id)

        if self._devices.Device.fetch({"id": id}):
            return

        device = self._devices.Device()
        device.update(attributes)
        device.id = id
        device._last_updated = int(time())
        device.update(self._base_query())
        device.save()

    def update(self, device, attributes):
        attributes.update({"_last_updated": int(time())})
        return self._devices.update({'_id': device['_id']}, {'$set': attributes})

    def save(self, device):
        if device:
            return device.save()
        return False

    def delete(self, device):
        query = {'_id': device['_id']}
        query.update(self._base_query())
        return self._devices.remove(query)

    def update_infos(self, device, data):
        device = self.device(device.id)

        if not device:
            return False

        self.update(device, {'infos': data})

    def equals(self, a, b):
        for k in ["connected", "params", "infos"]:
            if a[k] != b[k]:
                return False
        return True

    def do(self, device, action, **kwargs):
        pass
