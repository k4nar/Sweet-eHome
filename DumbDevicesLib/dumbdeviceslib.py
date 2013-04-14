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
        self.base_url = "http://{}:{}/api".format(self.address, self.port)

        self.dumb_action_to_action = {
            "turnOn": "on",
            "turnOff": "off",
        }

        self.action_to_dumb_action = dict([(v, k) for k, v in self.dumb_action_to_action.iteritems()])

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
        r = requests.post(self._url("devices", device["id"], action), data=kwargs)
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

        print action_name
        return self._post(device, action_name, **kwargs)
