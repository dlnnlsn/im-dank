import json


def convert_object(obj):
    if hasattr(obj, '__json__'):
        return obj.__json__()
    return repr(obj)


def serialize(obj):
    return json.dumps(obj, default=convert_object).encode('utf-8')
