import json

from light import Light
from switch import Switch

from device import DeviceEncoder


devices = dict((dev.id, dev) for dev in [
    Light(id="light"),
    Light(id="colorLight", changeColor=True, color="red"),
    Light(id="dummedLight", dummer=True, var=1.0),
    Light(id="complexLight", dummer=True, var=0.8, changeColor=True, color="blue"),
    Switch(id="switch1"),
    Switch(id="switch2")
])

def dumps(data):
    return json.dumps(data, cls=DeviceEncoder)
