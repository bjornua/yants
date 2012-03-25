# -*- coding: utf-8 -*-
from werkzeug.routing import Map, Rule
import logging

from functools import wraps

log = logging.getLogger(__name__)

url_map = Map()
endpts = {}

def mapto(method, path):
    def decorator(f):
        module = f.__module__.split(".")[-1]
        endpoint = "{}.{}".format(module, f.__name__)
        endpts[endpoint] = f
        url_map.add(Rule(path, methods=[method], endpoint=endpoint))
        return f
    return decorator

_static_adapter = url_map.bind("", "/")
def urlfor(endpoint, method=None, _external=False, **values):
    return _static_adapter.build(endpoint, values, method=method, force_external=_external)
