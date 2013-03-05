from bottle import Bottle, HTTPError, request

from core import devices, dumps

api = Bottle()


@api.get('/devices')
def get_all_devices():
    return dumps(devices.values())


@api.get('/devices/<id>')
def get_device_by_id(id):
    if id in devices:
        return dumps(devices[id])
    else:
        raise HTTPError(404)


@api.post('/devices/<id>/<action>')
def do_action(id, action):
    device = devices.get(id)
    if not device:
        raise HTTPError(404)

    kwargs = dict(request.forms.items())

    res = device(action, **kwargs)
    if not res:
        raise HTTPError(400)

    return dumps(res)


@api.get('/<type>')
def get_all_by_type(type):
    return dumps([dev for dev in devices.values() if dev.type == type])


api.run(host='localhost', port=4224, reloader=True)
