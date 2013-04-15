from DomoLib import BaseDriver

import openzwave
from openzwave import PyManager


class Driver(BaseDriver):

    name = "ZwaveDriver"
        
    def __init__(self):
        super(Driver, self).__init__()

        self.options = openzwave.PyOptions()
        self.options.create("src/libs/ZwaveLib/config/", "", "")
        self.options.lock()

        self.manager = openzwave.PyManager()
        self.manager.create()

        self.manager.addWatcher(self.receive)
        self.manager.addDriver('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0')

        self.actions = {
            "on" : self._turnOn,
            "off" : self._turnOff,
            "variate" : self._variate,
            }

    def _turnOn(self, device, **kwargs):
        self.manager.SetNodeOn(device['params']['homeId'], int(device['id']))

    def _turnOff(self, device, **kwargs):
        self.manager.SetNodeOff(device['params']['homeId'], int(device['id']))

    def _variate(self, device, **kwargs):
        self.manager.SetNodeLevel(device['params']['homeId'], int(device['id']), kwargs['var'])

    def _serialize(self, args):
        return {"id": str(args['nodeId']),
                "connected": True,
                "params": {"value": args['valueId']['value'],
                           "homeid": args['homeId']
                           }
                }
    
    def _notification(self, serialized_device):
        device = self.device(serialized_device["id"])
        if device:
            self.update(device, serialized_device)
        else:
            self.new(serialized_device)

    def receive(self, args):
        self._notification(self._serialize(args))

    def do(self, device, action, **kwargs):
        self.actions[action["name"]](device, action, kwargs)
