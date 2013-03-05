import requests

from DomoLib import BaseLib

class DumbDevicesLib(BaseListener):
    """
    Implementation of DomoLib for DumbDevices protocol
    """
    def __init__(self, core):
        super(Listener, self).__init__(core)

        self.address = "127.0.0.1"
        self.port = "4224"
        self.base_url = "http://" + self.address + ":" + self.port

    def _post(self, device, action, **kwargs):
        return request.post(self.base_url + "/" + device.id + "/" + action, data=kwargs)

    def do(self, device, action, **kwargs):
        r = _post(device, action, **kwargs)
        