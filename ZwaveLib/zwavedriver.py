from DomoLib import BaseDriver

import openzwave
from openzwave import PyManager


class Driver(BaseDriver):
    def __init__(self, core):
        super(Driver, self).__init__(core)

        self.name = "ZwaveDriver"

        self.options = openzwave.PyOptions()
        self.options.create("ZwaveLib/openzwave/config/", "", "")
        self.options.lock()

        self.manager = openzwave.PyManager()
        self.manager.create()

        self.manager.addWatcher(self.receive)
        self.manager.addDriver('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0')

    def receive(self, args):
        if args['notificationType'] == "NodeNew":
            attributes = {"id": str(args['nodeId']),
                          "type": "basic",
                          "params": {"value": args['valueId']['value']}}
            self.new(attributes)
        elif args['notificationType'] == "ValueAdded":
            device = self.device(str(args['nodeId']))
            if device:
                self.update(device, {"type": args['label'],
                                     "params": {"value": args['valueId']['value']}})
            else:
                raise Exception
        elif args['notificationType'] == "ValueChanged":
            device = self.device(str(args['nodeId']))
            if device:
                self.update(device, {"params": {"value": args['valueId']['value']}})
            else:
                raise Exception

    def do(self, device, action, **kwargs):
        print kwargs
