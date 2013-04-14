from multiprocessing.managers import BaseManager

from logger import logger

class Core(object):
    def __init__(self):
        super(Core, self).__init__()

        self.logger = logger
        self.wrappers = self.get_all_wrappers()

    def do(self, device, action, **kwargs):
        print self.wrappers
        driver = device["driver"]
        if not driver in self.wrappers:
            return False

        for arg in action["args"]:
            if not arg in kwargs:
                return False

        return self.wrappers[driver].do(device, action, **kwargs)



    def get_all_wrappers(self):
        from libs import libs

        wrappers = {}

        for lib in libs:
            try:
                driver = __import__(lib).Driver(self)
                wrappers[driver.name] = driver

            except Exception, e:
                self.logger.warning("Can't import module {}: {}".format(lib, e))

        return wrappers

class CoreManager(BaseManager):
    def __init__(self):
        super(CoreManager, self).__init__()

        self.register('Core', Core)
        self.start()

ProxyCore = CoreManager().Core
