import types

_CONTEXT_PROCESSORS_ATTR = '__processors__'


def get_context_processors(mixed):
    if isinstance(mixed, types.FunctionType):
        yield from getattr(mixed, _CONTEXT_PROCESSORS_ATTR, ())

    for cls in reversed((mixed if isinstance(mixed, type) else type(mixed)).__mro__):
        yield from cls.__dict__.get(_CONTEXT_PROCESSORS_ATTR, ())

    return ()


class ContextProcessor:
    @property
    def __name__(self):
        return self.func.__name__

    def __init__(self, func):
        self.func = func

    def __repr__(self):
        return repr(self.func).replace('<function', '<{}'.format(type(self).__name__))

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)


def contextual(cls_or_func):
    if isinstance(cls_or_func, types.FunctionType):
        try:
            getattr(cls_or_func, _CONTEXT_PROCESSORS_ATTR)
        except AttributeError:
            setattr(cls_or_func, _CONTEXT_PROCESSORS_ATTR, [])
        return cls_or_func

    if not _CONTEXT_PROCESSORS_ATTR in cls_or_func.__dict__:
        setattr(cls_or_func, _CONTEXT_PROCESSORS_ATTR, [])
    _processors = getattr(cls_or_func, _CONTEXT_PROCESSORS_ATTR)
    for name, value in cls_or_func.__dict__.items():
        if isinstance(value, ContextProcessor):
            _processors.append(value)
    return cls_or_func