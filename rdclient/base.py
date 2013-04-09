def method(result, **spec):
    """Decorator for declaring method"""
    def decorator(fnc):
        """Set spec to method"""
        fnc.spec = {
            'args': spec,
            'result': result,
        }
        fnc._is_device_method = True
        return fnc
    return decorator


class DeviceMethod(object):
    """Device method"""

    def __init__(self, fnc):
        self._fnc = fnc
        self.spec = fnc.spec
        self.name = fnc.func_name
        self.description = fnc.func_doc


class BaseDevice(type):
    """Device metaclass"""

    def __new__(cls, name, bases, dct):
        """Register device and methods"""
        device_cls = super(BaseDevice, cls).__new__(
            cls, name, bases, dct,
        )
        items = []
        for cls in device_cls.__mro__:
            items += cls.__dict__.items()
        for key, value in items:
            if getattr(value, '_is_device_method', False):
                device_cls._register_method(value)
        if not getattr(device_cls.Meta, 'abstract', False):
            Device.device = device_cls
        return device_cls

    def _register_method(cls, fnc):
        """Register method"""
        if not hasattr(cls, '_methods'):
            cls._methods = []
        cls._methods.append(
            DeviceMethod(fnc),
        )

    def declarations(cls):
        """Get methods declaration"""
        for method in cls._methods:
            yield {
                'uuid': cls.Meta.uuid,
                'spec': method.spec,
                'name': method.name,
                'description': method.description,
            }


class Device(object):
    """Device class"""
    __metaclass__ = BaseDevice

    def __init__(self, client):
        self._client = client

    def process_request(self, request):
        """Process request and send response"""
        try:
            print request
            method = getattr(self, request['method'])
            result = method(**request['request'])
            self.send_response(result, request['request_id'])
        except Exception as e:
            # fail silently
            print e
            pass

    def send_response(self, result, request_id):
        """Send response"""
        self._client.send(
            request_id=request_id,
            action='response',
            response=result,
            uuid=self.Meta.uuid,
        )

    class Meta:
        abstract = True
