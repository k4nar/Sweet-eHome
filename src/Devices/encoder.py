from device import Device
import json

class DevicesEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Device):
            return super(json.JSONDecoder, self).default(obj)

        return __encode(obj)

    def __encode(self, device):
        out = {}
        out["url"] = "/devices/{}".format(device.id)
        out["driver"] = device.driver
        out["actions"] = self.__encode_actions(device.actions)
        out["params"] = self.__encode_params(device.params)
        out["infos"] = self.__encode_infos(device.infos)

    def __encode_actions(self, actions):
        pass

    def __encode_params(self, params):
        pass

    def __encode_infos(self, infos):
        pass

class ShortenDevicesEncoder(DevicesEncoder):
    def __encode_actions(self, actions):
        pass

    def __encode_params(self, params):
        pass

    def __encode_infos(self, infos):
        pass