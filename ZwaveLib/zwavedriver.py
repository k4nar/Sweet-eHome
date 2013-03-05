from DomoLib import BaseDriver

import openzwave
from openzwave import PyManager


class zwaveDriver(BaseDriver):
    def __init__(self, core):
        super(zwaveDriver, self).__init__(core)

        self.options = openzwave.PyOptions()
        self.options.create("openzwave/config/", "", "")
        self.options.lock()
        
        self.manager = openzwave.PyManager()
        self.manager.create()

        self.manager.addWatcher(self.receive)
        self.manager.addDriver('/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0')

    def receive(self, args):
        if args['notificationType'] == "NodeNew" :
            attributes = { "id": args['nodeId'],
                           "type": "basic",
                           "params": { "value":args['valueId']['value'] } }
            self.new(self, attributes)
        else if args['notificationType'] == "ValueAdded" :
            device = self.device(self, args['nodeId'])
            if device :
                self.update(self, device, {"type":args['label'],
                                           "params" : { "value":args['valueId']['value'] } })
        else if args['notificationType'] == "ValueChanged" :
            device = self.device(self, args['nodeId'])
            if device :
                self.update(self, device, {"params" : { "value":args['valueId']['value'] } })
        print args

    def do(self, device, action, **kwargs):
        print kwargs
