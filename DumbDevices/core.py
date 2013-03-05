import json

from light import Light

from device import DeviceEncoder


devices = dict((dev.id, dev) for dev in [
    Light(id="light"),
    Light(id="colorLight", changeColor=True, color="red"),
    Light(id="dummedLight", dummer=True, var=1.0),
    Light(id="complexLight", dummer=True, var=0.8, changeColor=True, color="blue"),
])

def dumps(data):
    return json.dumps(data, cls=DeviceEncoder)
