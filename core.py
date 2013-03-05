from multiprocessing.managers import BaseManager

class Core(object):
    def __init__(self):
        super(Core, self).__init__()

        self.nb = 0

    def test(self, foo="FOO"):

        import time

        while 1:
            print "HELLO, I'M", foo, '--', self.nb
            self.nb += 1
            time.sleep(1)


class CoreManager(BaseManager):
    def __init__(self):
        super(CoreManager, self).__init__()

        self.register('Core', Core)
        self.start()

ProxyCore = CoreManager().Core
