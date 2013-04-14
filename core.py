from multiprocessing.managers import BaseManager

from wrappers import get_all_wrappers

class Core(object):
    def __init__(self):
        super(Core, self).__init__()

        self.wrappers = get_all_wrappers(self)

    def do(self, device, action, **kwargs):
        driver = device["driver"]
        if not driver in self.wrappers:
            return False

        return self.wrappers[driver].do(device, action, **kwargs)

    def set_wrappers(wrappers):
        self.wrappers = wrappers

class CoreManager(BaseManager):
    def __init__(self):
        super(CoreManager, self).__init__()

        self.register('Core', Core)
        self.start()

ProxyCore = CoreManager().Core
