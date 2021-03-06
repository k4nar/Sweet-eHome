import json

from bottle import Bottle, response, request

from Devices import Device, Action

api = Bottle()
root = Bottle()
root.mount('/api/v1', api)


def run(core):
    api.core = core
    root.run(host='0.0.0.0', port=1337)


@api.error(400)
@api.error(405)
@api.error(500)
def error_handler(error):
    enable_cors()
    response.content_type = "application/json"
    return json.dumps({"error": "Internal Server Error."})


@api.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With'
    response.headers['Access-Control-Allow-Origin'] = '*'


# Devices routes ####


@api.get('/devices')
def get_devices():
    query = {}
    for k in request.params.keys():
        query[k] = request.params.get(k)
    return {"devices": Device.all_to_api(query)}


@api.route('/devices', method=['POST', 'OPTIONS'])
def query_devices():
    return {"devices": Device.all_to_api(request.json)}


@api.get('/devices/<id>')
def get_device(id):
    device = Device.to_api(id)
    if device:
        return device
    else:
        response.status = 404
        return {"error": "Device {} not found.".format(id)}


@api.get('/devices/<id>/params')
def get_device_params(id):
    device = Device.to_api(id)
    if device:
        return device["params"]
    else:
        response.status = 404
        return {"error": "Device {} not found.".format(id)}


@api.get('/devices/<id>/params/<name>')
def get_device_params(id, name):
    device = Device.to_api(id)
    if device:
        if device["params"].has_key(name):
            return {name: device["params"][name]}
        else:
            response.status = 404
            return {"error": "Params {} not found in device {}.".format(name, id)}
    else:
        response.status = 404
        return {"error": "Device {} not found.".format(id)}


# Action routes ####


@api.get('/actions')
def get_actions():
    query = {}
    for k in request.params.keys():
        query[k] = request.params.get(k)
    return {"actions": Action.all_to_api(query)}


@api.route('/actions', method=['POST', 'OPTIONS'])
def query_devices():
    return {"actions": Device.all_to_api(request.json)}


@api.get('/actions/<name>')
def get_action(name):
    action = Action.to_api(name)
    if action:
        return action
    else:
        response.status = 404
        return {"error": "Action {} not found.".format(name)}


@api.get('/devices/<id>/actions')
def get_device_action(id):
    device = Device.to_api(id)
    if device:
        return {"actions": device["actions"]}
    else:
        response.status = 404
        return {"error": "Device {} not found.".format(id)}


@api.route('/devices/<id>/actions/<name>', method=['POST', 'OPTIONS'])
def post_action(id, name):
    device = Device.to_api(id)
    action = Action.to_api(name)
    if device and action:
        if not device["connected"]:
            response.status = 403
            return {"error": "Device {} is not connected.".format(id)}

        args = dict([(arg, request.json.get(arg)) for arg in action["args"]])

        if api.core.do(device, action, **args):
            response.status = 204
        else:
            response.status = 403
            return {"error": "Impossible to do action {} for device {} with args {}".format(name, id, args)}
    else:
        response.status = 404
        return {"error": "Device {} not found.".format(id)}


# User information routes ####


@api.get('/devices/<id>/infos')
def get_device_infos(id):
    device = Device.to_api(id)
    if device:
        return device["infos"]
    else:
        response.status = 404
        return {"error": "Device {} not found.".format(id)}


@api.route('/devices/<id>/infos', method=['POST', 'OPTIONS'])
def post_device_infos(id):
    device = Device.to_api(id)
    if device:
        infos = request.json
        if not infos:
            response.status = 204
            return
        if api.core.update_infos(device, infos):
            response.status = 204
        else:
            response.status = 403
            return {"error": "Impossible to set infos for device {}".format(id)}
    else:
        response.status = 404
        return {"error": "Device {} not found.".format(id)}


# Updates routes ####


@api.get('/updates/<since>')
def get_updates(since):
    return {"devices": Device.get_updated_since(int(since))}
