from multiprocessing import Process

from server import run
from core import ProxyCore

from logger import logger

if __name__ == '__main__':

    core = ProxyCore()

    from Devices.action import init_actions
    init_actions()

    server = Process(target=run, args=(core,))
    server.start()
    server.join()
