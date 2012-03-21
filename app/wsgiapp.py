# -*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from os.path import join

from werkzeug import Request, Response, SharedDataMiddleware
from werkzeug.exceptions import NotFound

from app.mapping import url_map, endpts
from app.utils.misc import local, path

import app.config
config = app.config.get()

class Main(object):
    def __init__(self, debug):
        local.application = self
        self.debug = debug
        self.dispatch = SharedDataMiddleware(self.safedispatch, {"/static": path["static"]})
    
    def safedispatch(self, environ, start_response):
        try:
            return self.appdispatch(environ, start_response)
        except: 
            if self.debug:
                raise
            log.exception("Exception")
            return Response("Fejlsidens fejlside.")(environ, start_response)

    def appdispatch(self, environ, start_response):
        local.request = Request(environ)
        local.response = Response()
        try:
            local.url_adapter = url_adapter = url_map.bind_to_environ(environ)
            try:
                endpt, params = url_adapter.match()
            except NotFound:
                endpt, params = "notfound", {}
            local.endpt = endpt
            endpts[endpt](**params)
        except:
            if self.debug:
                raise
            else:
                log.exception(
                    "Exception in %s with params %s",
                    endpt, repr(params)
                )
                local.endpt = "error"
                endpts["error"]()
        response = local.response
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        local.application = self
        return self.dispatch(environ, start_response)
