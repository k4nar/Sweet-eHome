import time

from multiprocessing import Process

import requests

from DomoLib import BaseDriver

STATUS_OK = 200


class Driver(BaseDriver):
    """
    Implementation of DomoLib driver for DumbDevices protocol
    """

    name = "DumbDevicesDriver"

    address = "127.0.0.1"
    port = "4224"
    base_url = "http://{}:{}/api".format(address, port)

    ERROR_NO_CONNECTION = "Can't connect to DumbDevices server at {}:{}".format(address, port)

    dumb_action_to_action = {
        "turnOn": "on",
        "turnOff": "off",
    }

    action_to_dumb_action = dict([(v, k) for k, v in dumb_action_to_action.iteritems()])

    def __init__(self):
        super(Driver, self).__init__()

        self.broadcaster = Process(target=self._broadcaster)
        self.broadcaster.start()


    def _url(self, *args):
        return "/".join([self.base_url] + list(args))

    def _get_dumb_devices(self):
        try:
            r = requests.get(self._url("devices"))
        except:
            self.core.logger.error(self.ERROR_NO_CONNECTION)
            return None

        if r.status_code != STATUS_OK:
            return None

        return r.json()

    def _get_dumb_device(self, id):
        try:
            r = requests.get(self._url("devices", id))
        except:
            self.core.logger.error(self.ERROR_NO_CONNECTION)
            return None

        if r.status_code != STATUS_OK:
            return None

        return r.json()

    def _post(self, device, action, **kwargs):
        try:
            r = requests.post(self._url("devices", device["id"], action), data=kwargs)
        except:
            self.core.logger.error(self.ERROR_NO_CONNECTION)
            return False

        if r.status_code == STATUS_OK:
            return True

        return False

    def _get_action(self, name):
        if name in self.dumb_action_to_action:
            name = self.dumb_action_to_action[name]

        return self.action(name)

    def _serialize(self, dumb_device):
        actions = []
        for name in dumb_device["actions"].keys():
            action = self._get_action(name)
            if action:
                actions.append(action)

        if "on" and "off" in actions:
            actions.append(self.action("toggle"))

        return {
            "id": dumb_device["id"],
            "params": dumb_device["properties"],
            "actions": actions,
            "infos": {"type": dumb_device["type"]}
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
            devices = self._get_dumb_devices()
            if devices:
                for device in devices:
                    self._store(device)

    def do(self, device, action, **kwargs):
        action_name = action["name"]
        if action_name in self.action_to_dumb_action:
            action_name = self.action_to_dumb_action[action_name]

        return self._post(device, action_name, **kwargs)

