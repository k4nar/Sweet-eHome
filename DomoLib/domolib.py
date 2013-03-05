from Devices.device import devices

class BaseDriver(object):
    """Base class for DomoLib drivers implementations"""
    def __init__(self, core):
        super(BaseDriver, self).__init__()
        
        self.name = "BaseDriver"

        self._core = core
        self._devices = devices

    def _base_query(self):
        return {'driver': self.name}

    def devices(self, query=None):
        if query:
            query.update(self._base_query())
        else:
            query = self._base_query()

        return self._devices.find(query)

    def device(self, id):
        query = {'id': id}
        query.update(self._base_query())

        return self._devices.find_one(query)

    def new(self, attributes):
        device = self._devices.StoredDevice()
        device.update(attributes)
        device.update(self._base_query())
        device.save()

    def update(self, device, attributes):
        return self._devices.update({'_id': device['_id']}, {'$set': attributes})
    
    def save(self, device):
        if device:
            return device.save()
        return False

    def delete(self, device):
        query = {'_id': device['_id']}
        query.update(self._base_query())
        return self._devices.remove(query)

    def do(self, device, action, **kwargs):
        pass
