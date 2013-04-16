from DomoLib import BaseDriver

import openzwave
from openzwave import PyManager


class Driver(BaseDriver):

    name = "ZwaveDriver"
        
    def __init__(self):
        super(Driver, self).__init__()

        self.options = openzwave.PyOptions()
        self.options.create("src/libs/ZwaveLib/config/", "src/libs/ZwaveLib/user/", "")
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
        actions = []
        actions.append(self.action("on"))
        actions.append(self.action("off"))
        actions.append(self.action("variate"))
        arguments = { "connected": False,
                      "actions": actions,
                      "params": {"homeid": args['homeId']}
                      }
        device = self.device(str(args["nodeId"]))
        if device:
            self.update(device, arguments)
        else:
            self.new(args['nodeId'], arguments)

    def _updateValue(self, args):
        if (args['valueId'] and (args['valueId']['label'] == "Basic"
                                or args['valueId']['label'] == "Level")):
            device = self.device(str(args["nodeId"]))
            if device and args['valueId']['label'] == "Sensor":
                arguments = { "connected": True,
                              "params": {"value": args['valueId']['value'],
                                         "actions": [],
                                         "homeId": args['homeId']}
                              }
                self.update(device, arguments)
            elif device:
                arguments = { "connected": True,
                              "params": {"value": args['valueId']['value'],
                                         "homeId": args['homeId']}
                              }
                self.update(device, arguments)
            else:
                raise Exception
            

    def _turnOn(self, device, **kwargs):
        self.manager.setNodeOn(device['params']['homeId'], int(self.get_id(device)))
        return True

    def _turnOff(self, device, **kwargs):
        self.manager.setNodeOff(device['params']['homeId'], int(self.get_id(device)))
        return True

    def _variate(self, device, **kwargs):
        try:
            print kwargs
            self.manager.setNodeLevel(device['params']['homeId'], int(self.get_id(device)), int(kwargs['var']))
            return True
        except:
            return False

    def receive(self, args):
        self.notifications[args['notificationType']](args)

    def do(self, device, action, **kwargs):
        return self.actions[action["name"]](device, **kwargs)
