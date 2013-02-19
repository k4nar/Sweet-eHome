from multiprocessing import Process, Pipe
import time

class BaseBroadcaster(Process):
    """
    Base class for broadcaster
    """

    def __init__(self):
        super(BaseBroadcaster, self).__init__()

        self.sleep_time = 200

    def run(self):
        """
        Main loop of the process, called from Process.start
        """

        while 1:
            self.broadcast()
            self.wait()

    def wait(self):
        """
        Called by run to pause the main loop in order to avoid CPU bounds
        """
        time.sleep(self.sleep_time)

    def broadcast(self):
        pass
