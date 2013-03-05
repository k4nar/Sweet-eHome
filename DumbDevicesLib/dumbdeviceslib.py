import time

from multiprocessing import Process

import requests

from DomoLib import BaseDriver

STATUS_OK = 200


class Driver(BaseDriver):
    """
    Implementation of DomoLib driver for DumbDevices protocol
    """
    def __init__(self, core):
        super(Driver, self).__init__(core)

        self.name = "DumbDevicesDriver"

        self.address = "127.0.0.1"
        self.port = "4224"
        self.base_url = "http://{}:{}".format(self.address, self.port)

        self.broadcaster = Process(target=self._broadcaster)
        self.broadcaster.start()

    def _url(self, *args):
        return "/".join([self.base_url] + list(args))

    def _get_dumb_devices(self):
        r = requests.get(self._url("devices"))

        if r.status_code != STATUS_OK:
            return None

        return r.json()

    def _get_dumb_device(self, id):
        r = requests.get(self._url("devices", id))

        if r.status_code != STATUS_OK:
            return None

        return r.json()

    def _post(self, device, action, **kwargs):
        r = requests.post(self._url("devices", device.id, action), data=kwargs)
        if r.status_code == STATUS_OK:
            return True
        return False

    def _serialize(self, dumb_device):
        actions = [{"name": name, "args": args} for name, args in dumb_device["actions"].items()]

        return {
            "type": dumb_device["type"],
            "id": dumb_device["id"],
            "params": dumb_device["properties"],
            #"actions": actions,
        }

    def _store(self, dumb_device):
        p = self._serialize(dumb_device)

        device = self.device(dumb_device["id"])

        if device:
            return self.update(device, p)
        else:
            return self.new(p)

    def _broadcaster(self):
        while 1:
            time.sleep(1)
            print "Broadcasting..."
            devices = self._get_dumb_devices()
            if devices:
                for device in devices:
                    self._store(device)

    def do(self, device, action, **kwargs):
        return self._post(device, action, **kwargs)
