# -*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from werkzeug import Request, Response, SharedDataMiddleware
from werkzeug.exceptions import NotFound

from app.mapping import url_map, endpts

import app.config
config = app.config.get()

def Main(debug):
    dispatch = AppMiddleware(None, debug)
    dispatch = SharedDataMiddleware(dispatch, {"/static": "static"})
    dispatch = ErrorMiddleware(dispatch, debug)

    return dispatch

def ErrorMiddleware(target, debug):
    def dispatch(environ, start_response):
        try:
            return target(environ, start_response)
        except: 
            if debug:
                raise
            log.exception("Exception")
            return Response("Fejlsidens fejlside.")(environ, start_response)

    return dispatch

def AppMiddleware(target, debug):
    @Request.application
    def dispatch(request):
        url_adapter = url_map.bind_to_environ(request.environ)
        try:
            endpt, params = url_adapter.match()
        except NotFound:
            endpt, params = "notfound", {}
        
        try:
            return endpts[endpt](request=request, **params)
        except:
            if debug:
                raise
            else:
                log.exception("Exception in %s with params %s", endpt, repr(params))
                return endpts["error"](request = request)

    return dispatch
