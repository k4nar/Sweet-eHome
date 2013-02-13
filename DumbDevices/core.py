import sys
import json
from light import Light
from device import DeviceEncoder


devices = dict((dev.id, dev) for dev in [
    Light(id="light"),
    Light(id="colorLight", changeColor=True, color="red"),
    Light(id="dummedLight", dummer=True, var=1.0),
    Light(id="complexLight", dummer=True, var=0.8, changeColor=True, color="blue"),
])


def handle_device(id, *args):
    if id in devices and devices[id](*args):
        print "OK"
    else:
        print "FAIL"


def print_device(id, *args):
    if id in devices:
        print json.dumps(devices[id], cls=DeviceEncoder)
    else:
        print "Device", id, "not found."


def monitor(*args):
    print json.dumps(devices.values(), cls=DeviceEncoder)


handlers = {
    "set": handle_device,
    "print": print_device,
    "monitor": monitor,
}


def handle(op, *args):
    if op in handlers:
        handlers[op](*args)
    else:
        print "No such operator", op, "."

if __name__ == '__main__':
    while True:
        line = sys.stdin.readline()
        handle(*line.split())
