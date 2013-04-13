from bottle import Bottle, HTTPError

from Devices import Device, Action

api = Bottle()

def run(core):
    api.run(host='localhost', port=1337)

#### Devices routes ####

@api.get('/devices')
def get_devices():
    return {"devices": Device.all()}

@api.get('/devices/<id>')
def get_device(id):
    device = Device.by_id(id)
    if device:
        return device
    else:
        return HTTPError(404)

@api.get('/devices/<id>/params')
def get_device_params(id):
    device = Device.by_id(id)
    if device:
        return device["params"]
    else:
        return HTTPError(404)

@api.get('/devices/<id>/params/<name>')
def get_device_params(id, name):
    device = Device.by_id(id)
    if device:
        if device.params.has_key(name):
            return {name: device["params"][name]}
        else:
            return HTTPError(404)
    else:
        return HTTPError(404)


#### Action routes ####

@api.get('/actions')
def get_actions():
    return {"actions": Action.all()}

@api.get('/actions/<name>')
def get_action(name):
    action = Action.by_name(name)
    if action:
        return action
    else:
        return HTTPError(404)

@api.get('/devices/<id>/actions')
def get_device_action(id):
    device = Device.by_id(id)
    if device:
        return {"actions": device["actions"]}
    else:
        return HTTPError(404)

@api.post('/devices/<id>/actions/<name>')
def post_action(id, name):
  return ""


#### User information routes ####

@api.get('/devices/<id>/infos')
def get_device_infos(id):
    device = Device.by_id(id)
    if device:
        return device["infos"]
    else:
        return HTTPError(404)

@api.post('/devices/<id>/infos/<name>')
def post_device_infos(id, name):
    return ""
