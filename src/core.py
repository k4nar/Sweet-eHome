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
        drivers = []

        class DriverManager(BaseManager):
            pass

        for lib in libs:
            try:
                driver = import_module("libs.{}".format(lib)).Driver
                DriverManager.register(driver.name, driver)
                drivers.append(driver.name)
            except Exception, e:
                self.logger.warning("Can't import module {}: {}".format(lib, e))

        manager = DriverManager()
        manager.start()

        for name in drivers:
            try:
                wrappers[name] = manager.__getattribute__(name)()
            except Exception, e:
                self.logger.warning("Can't start {}: {}".format(driver, e))

        return wrappers

    def update_infos(self, device, data):
        driver = device["driver"]
        wrapper = self.wrappers.get(driver)

        if not wrapper:
            return False

        return wrapper.update_infos(device, data)


class CoreManager(BaseManager):
    def __init__(self):
        super(CoreManager, self).__init__()

        self.register('Core', Core)
        self.start()

ProxyCore = CoreManager().Core
