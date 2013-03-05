from multiprocessing import Process, Pipe
import time

class BaseListener(Process):
    """
    Base class for listeners
    """
    def __init__(self, core):
        super(BaseListener, self).__init__()
        
        self.core = core

        # Create the connections for the core and the child process
        self.listener_conn, self.core_conn = Pipe(duplex=False)

        self.sleep_time = 0.01

    def start(self):
        super(BaseListener, self).start()
        self.listener_conn.close()

    def run(self):
        """
        Main loop of the process, called from Process.start
        """
        self.core_conn.close()

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

    def send(self, *args):
        """
        Sends args to the Core
        """
        self.listener_conn.send(args)

    def read(self):
        """
        Read message from child
        """
        return self.core_conn.recv()
