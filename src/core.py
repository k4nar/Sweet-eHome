from multiprocessing.managers import BaseManager
from importlib import import_module

from libs import libs

from logger import logger

class Core(object):
    def __init__(self):
        super(Core, self).__init__()

        self.logger = logger
        self.wrappers = self.get_all_wrappers()

    def do(self, device, action, **kwargs):
        driver = device["driver"]
        if not driver in self.wrappers:
            return False

        for arg in action["args"]:
            if not arg in kwargs:
                return False

        return self.wrappers[driver].do(device, action, **kwargs)

    def get_all_wrappers(self):


        wrappers = {}

        for lib in libs:
            try:
                driver = import_module("libs.{}".format(lib)).Driver(self)
                wrappers[driver.name] = driver

            except Exception, e:
                self.logger.warning("Can't import module {}: {}".format(lib, e))

        return wrappers

    def update_infos(self, device, data):
        driver = device["driver"]
        wrapper = self.wrappers.get(driver)

        if not wrapper:
            return False

        return devices.update_infos(device, data)


class CoreManager(BaseManager):
    def __init__(self):
        super(CoreManager, self).__init__()

        self.register('Core', Core)
        self.start()

ProxyCore = CoreManager().Core
