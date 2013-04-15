from bottle import Bottle, response

from Devices import Device, Action

api = Bottle()
root = Bottle()
root.mount('/api/v1', api)


def run(core):
    api.core = core

    root.run(host='localhost', port=1337)

@api.error(403)
@api.error(404)
@api.error(204)
def error_handler(error):
    enable_cors()
    return api.default_error_handler(error)

@api.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With'
    response.headers['Access-Control-Allow-Origin'] = '*'

#### Devices routes ####

@api.get('/devices')
def get_devices():
    return {"devices": Device.all_to_api()}

@api.get('/devices/<id>')
def get_device(id):
    device = Device.to_api(id)
    if device:
        return device
    else:
        response.status = 404

@api.get('/devices/<id>/params')
def get_device_params(id):
    device = Device.to_api(id)
    if device:
        return device["params"]
    else:
        response.status = 404


@api.get('/devices/<id>/params/<name>')
def get_device_params(id, name):
    device = Device.to_api(id)
    if device:
        if device["params"].has_key(name):
            return {name: device["params"][name]}
        else:
            response.status = 404
    else:
        response.status = 404


#### Action routes ####

@api.get('/actions')
def get_actions():
    return {"actions": Action.all_to_api()}

@api.get('/actions/<name>')
def get_action(name):
    action = Action.to_api(name)
    if action:
        return action
    else:
        response.status = 404


@api.get('/devices/<id>/actions')
def get_device_action(id):
    device = Device.to_api(id)
    if device:
        return {"actions": device["actions"]}
    else:
        response.status = 404

@api.route('/devices/<id>/actions/<name>', method=['POST', 'OPTIONS'])
def post_action(id, name):
    device = Device.to_api(id)
    action = Action.to_api(name)
    if device and action:
        args = dict([(args, request.forms.get(arg)) for arg in action["args"]])
        if api.core.do(device, action, **args):
            response.status = 204
        else:
            response.status = 403
    else:
        response.status = 404


#### User information routes ####

@api.get('/devices/<id>/infos')
def get_device_infos(id):
    device = Device.to_api(id)
    if device:
        return device["infos"]
    else:
        response.status = 404

@api.route('/devices/<id>/infos', method=['POST', 'OPTIONS'])
def post_device_infos(id, name):
    device = Device.to_api(id)
    if device:
        return self.core.update_infos
    else:
        response.status = 404