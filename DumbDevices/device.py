import json
import inspect

class Device:
    def __init__(self, id=""):
        self.id = id
        self.type = ""
        self.actions = {}
        self.properties = {}

    def __call__(self, action, **kwargs):
        if action in self.actions:
            return self.actions[action](**kwargs)
        return False


class DeviceEncoder(json.JSONEncoder):
    def default(self, obj):
        if not isinstance(obj, Device):
            return super(json.JSONDecoder, self).default(obj)

        return {"type": obj.type, "id": obj.id, "properties": obj.properties, "actions": self.encode_actions(obj.actions)}

    def encode_actions(self, actions):
        d = {}
        
        for name, func in actions.items():
            args = inspect.getcallargs(func)
            args.pop("self")
            d[name] = args

        return d
