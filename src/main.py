#!/usr/bin/python2

from multiprocessing import Process

from server import run
from core import ProxyCore

if __name__ == '__main__':
    from Devices.device import disconnect_all
    disconnect_all()

    from Devices.action import init_actions
    init_actions()

    core = ProxyCore()

    server = Process(target=run, args=(core,))
    server.start()
    server.join()
