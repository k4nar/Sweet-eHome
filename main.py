from multiprocessing import Process

from wrappers import get_all_wrappers
from server import run
from core import ProxyCore

def proc1(core):
    core.test("proc1")


def proc2(core):
    core.test("proc2")


def proc3(core):
    core.test("proc3")


if __name__ == '__main__':

    core = ProxyCore()

    wrappers = get_all_wrappers(core)

    server = Process(target=run, args=(core,))
    server.start()
    server.join()
