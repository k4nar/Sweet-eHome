from multiprocessing import Process

from wrappers import get_all_wrappers
from server import run
from core import ProxyCore

if __name__ == '__main__':

    core = ProxyCore()

    wrappers = get_all_wrappers(core)

    from Devices.action import init_actions
    init_actions()

    server = Process(target=run, args=(core,))
    server.start()
    server.join()
