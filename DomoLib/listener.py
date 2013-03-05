from multiprocessing import Process
import time

class BaseListener(Process):
    """
    Base class for listeners
    """
    def __init__(self, core):
        super(BaseListener, self).__init__()
        
        self.core = core

        self.sleep_time = 0.01

    def run(self):
        """
        Main loop of the process, called from Process.start
        """
        while 1:
            self.listen()
            self.wait()

    def wait(self):
        """
        Called by run to pause the main loop in order to avoid CPU bounds
        """
        time.sleep(self.sleep_time)

    def listen(self):
        """
        Method that needs to be overloaded
        """
        pass

    def receive(self, *args, **kwargs):
        """
        Method that needs to be called every time you want to handle a response
        Starts `self.handler` in a new process
        """
        p = Process(target=self.handler, args=args, kwargs=kwargs)
        p.start()

    def handler(self, *args, **kwargs):
        """
        Method that needs to be overloaded
        Called in a new process every time receive is called 
        """
        pass
