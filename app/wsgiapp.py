# -*- coding: utf-8 -*-
import logging
log = logging.getLogger(__name__)

from werkzeug import Request, Response, SharedDataMiddleware
from werkzeug.exceptions import NotFound


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
        import app.controllers.document
        from app.controllers.error import notfound, error
        from app.mapping import url_map, endpts
        url_adapter = url_map.bind_to_environ(request.environ)
        
        try:
            try:
                endpt, params = url_adapter.match()
                return endpts[endpt](request=request, url_adapter=url_adapter, **params)
            except NotFound:
                return notfound(request=request, url_adapter=url_adapter)
        except:
            # Let werkzeug handle the exception
            if debug:
                raise
            
            # Log error and return error page
            log.exception("Exception in %s with params %s", endpt, repr(params))
            return error(request = request)

    return dispatch
