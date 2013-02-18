from multiprocessing import Process

import server
from wrappers import wrappers

if __name__ == '__main__':

    for wrapper in wrappers.values():
        wrapper['listener'].start()
        wrapper['broadcaster'].start()

    server = Process(target=server.run)
    server.start()
