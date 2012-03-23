# -*- coding: utf-8 -*-
from app.utils.misc import templateresponse

def error(**kwargs):
    return templateresponse("/error/servererror.mako")

def notfound(**kwargs):
    return templateresponse("/error/notfound.mako")

def notyet(**kwargs):
    return templateresponse("/error/notyet.mako")
