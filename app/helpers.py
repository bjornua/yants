# -*- coding: utf-8 -*-
import werkzeug
import werkzeug.utils
import json

from app.template import runtemplate
from app.mapping import urlfor

def templateresponse(templatename, **kwargs):
    response = werkzeug.Response()
    runtemplate(templatename, response, **kwargs)
    return response

def redirect(endpoint, *args, **kwargs):
    return werkzeug.utils.redirect(urlfor(endpoint, *args, **kwargs))

def jsonresponse(data, *args, **kwargs):
    response = werkzeug.Response()
    response.mime_type = "application/json"
    response.data = json.dumps(data)
    return response
