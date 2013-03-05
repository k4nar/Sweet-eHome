from DomoLib import BaseListener

import openzwave
from openzwave import PyManager


class Listener(BaseListener):
    def __init__(self, core):
        super(Listener, self).__init__(core)

        self.options = openzwave.PyOptions()
        self.options.create("openzwave/config/", "", "")
        self.options.lock()
        
        self.manager = openzwave.PyManager()
        self.manager.create()

        self.manager.addWatcher(self.receive)
        self.manager.addDriver(
            '/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0')

    def handler(self, args):
        print args
