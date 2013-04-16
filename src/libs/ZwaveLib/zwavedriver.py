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

        self.notifications = {
            "NodeNew" : self._updateNode,
            "NodeAdded" : self._updateNode,
            "ValueAdded" : self._updateValue,
            "ValueChanged" : self._updateValue,
            }

    def _updateNode(self, args):
        arguments = { "id": str(args['nodeId']),
                      "connected": False,
                      "params": {"homeid": args['homeId']}
                      }
        device = self.device(str(args["nodeId"]))
        if device:
            self.update(device, arguments)
        else:
            self.new(arguments)

    def _updateValue(self, args):
        if (args['valueId'] and (args['valueId']['label'] == "Basic"
                                or args['valueId']['label'] == "Level")):
            device = self.device(str(args["nodeId"]))
            if device:
                arguments = { "connected": True,
                              "params": {"value": args['valueId']['value']}
                              }
                self.update(device, arguments)
            else:
                raise Exception
            

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

    def receive(self, args):
        self.notifications[args['notificationType']](args)

    def do(self, device, action, **kwargs):
        self.actions[action["name"]](device, action, kwargs)
