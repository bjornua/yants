# -*- coding: utf-8 -*-
import werkzeug
from app.utils.misc import runtemplate

def error(request):
    response = werkzeug.Response()
    runtemplate(response, "/error/servererror.mako")
    return response

def notfound(request):
    response = werkzeug.Response()
    runtemplate(response, "/error/notfound.mako")
    return response

def notyet(request):
    response = werkzeug.Response()
    runtemplate(response, "/error/notyet.mako")
    return response

