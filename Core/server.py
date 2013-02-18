from bottle import Bottle

api = Bottle()

@api.get('/devices')
def get_all_devices():
    return ""


@api.get('/devices/<id>')
def get_device_by_id(id):
    return ""


@api.get('/<type>')
def get_all_by_type(type):
    return ""


@api.get('/<type>/<id>')
def get_type_by_id(type, id):
    return ""


@api.post('/devices/<id>')
def post_device(id):
    return ""


@api.put('/devices/')
def put_device():
    return ""


@api.delete('/devices')
def delete_devices():
    return ""


def run():
    api.run(host='localhost', port=1337, reloader=True)
