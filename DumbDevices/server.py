from bottle import Bottle, HTTPError, request, static_file, response

from core import devices, dumps

api = Bottle(autojson=True)


@api.get('/api/devices')
def get_all_devices():
    response.content_type = 'application/json'
    return dumps(devices.values())


@api.get('/api/devices/<id>')
def get_device_by_id(id):
    if id in devices:
        return dumps(devices[id])
    else:
        raise HTTPError(404)


@api.post('/api/devices')
@api.post('/api/devices/<id>/<action>')
def do_action(id, action):
    device = devices.get(id)
    if not device:
        raise HTTPError(404)

    kwargs = dict(request.forms.items())
    print kwargs
    # if kwargs.has_key("id"):
    #     kwargs.pop("id")
    # if kwargs.has_key("action"):
    #     kwargs.pop("action")
    # print kwargs

    res = device(action, **kwargs)
    if not res:
        raise HTTPError(400)

    return dumps(res)


@api.get('/api/<type>')
def get_all_by_type(type):
    response.content_type = 'application/json'
    return dumps([dev for dev in devices.values() if dev.type == type])

@api.get('/<filename:path>')
def static(filename):
    return static_file(filename, root='webui/')

@api.get('/')
def index():
    return static("index.html")

api.run(host='localhost', port=4224, reloader=True)
