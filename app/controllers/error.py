# -*- coding: utf-8 -*-
from app.utils.misc import template_response

def error():
    template_response("/error/servererror.mako")

def notfound():
    template_response("/error/notfound.mako")

def notyet():
    template_response("/error/notyet.mako")

