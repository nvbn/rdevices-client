import json


def method(result, **spec):
    def decorator(fnc):
        fnc.spec = {
            'args': spec,
            'result': result,
        }
        fnc._is_device_method = True
        return fnc
    return decorator


class DeviceMethod(object):
    def __init__(self, fnc):
        self._fnc = fnc
        self.spec = fnc.spec
        self.name = fnc.func_name
        self.description = fnc.func_doc


class BaseDevice(type):
    def __new__(cls, name, bases, dct):
        device_cls = super(BaseDevice, cls).__new__(
            cls, name, bases, dct,
        )
        for key, value in device_cls.__dict__.items():
            if getattr(value, '_is_device_method', False):
                device_cls._register_method(value)
        if not getattr(device_cls.Meta, 'abstract', False):
            Device.device = device_cls
        return device_cls

    def _register_method(cls, fnc):
        if not hasattr(cls, '_methods'):
            cls._methods = []
        cls._methods.append(
            DeviceMethod(fnc),
        )

    def declarations(cls):
        for method in cls._methods:
            yield {
                'uuid': cls.Meta.uuid,
                'spec': method.spec,
                'name': method.name,
                'description': method.description,
            }


class Device(object):
    __metaclass__ = BaseDevice

    def __init__(self, sock):
        self._sock = sock

    def process_request(self, request):
        try:
            method = getattr(self, request['method'])
            result = method(**request['request'])
            self.send_response(result, request['request_id'])
        except Exception:
            # fail silently
            pass

    def send_response(self, result, request_id):
        self._sock.write(json.dumps({
            'request_id': request_id,
            'action': 'response',
            'response': result,
            'uuid': self.Meta.uuid,
        }))

    class Meta:
        abstract = True
