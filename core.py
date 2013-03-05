from multiprocessing.managers import BaseManager

from Devices.device import devices

class Core(object):
    def __init__(self):
        super(Core, self).__init__()

        self.devices = devices


class CoreManager(BaseManager):
    def __init__(self):
        super(CoreManager, self).__init__()

        self.register('Core', Core)
        self.start()

ProxyCore = CoreManager().Core
