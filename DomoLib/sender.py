class BaseSender(object):
    """Base class for senders"""

    def __init__(self, core):
        super(BaseSender, self).__init__()

        self.core = core

    def send(self):
        pass

    def do(self, action, device):
        pass
