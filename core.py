from multiprocessing.managers import BaseManager

class Core(object):
    def __init__(self):
        super(Core, self).__init__()

        self.wrappers = {}

    def do(self, device, action, **kwargs):
        if not device.driver in self.wrappers:
            return False

        return self.wrappers[device.driver].do(device, action, **kwargs)

class CoreManager(BaseManager):
    def __init__(self):
        super(CoreManager, self).__init__()

        self.register('Core', Core)
        self.start()

ProxyCore = CoreManager().Core
