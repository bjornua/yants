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
            log.exception("WSGI Handler exception")
            return Response("Error.")(environ, start_response)

    return dispatch

def AppMiddleware(target, debug):
    @Request.application
    def dispatch(request):
        import app.controllers.document
        from app.controllers.error import notfound, error
        from app.mapping import url_map, endpts
        from app.utils.session import Session
        from app.db import sessiondb

        try:
            url_adapter = url_map.bind_to_environ(request.environ)

            session_id = request.cookies.get("session_id")
            if session_id is not None:
                try:
                    session_id = int(session_id)
                except ValueError:
                    session_id = None

            session_token = request.cookies.get("session_token")
            session = Session(sessiondb, session_id, session_token, ttl=60)

            try:
                endpt, params = url_adapter.match()
                response = endpts[endpt](request=request, url_adapter=url_adapter, session=session, **params)
            except NotFound:
                response = notfound(request=request, url_adapter=url_adapter)
            
            if session.token is None or session.id is None:
                return response

            response.set_cookie("session_id", unicode(session.id), max_age=99999999)
            response.set_cookie("session_token", session.token, max_age=99999999)
            return response
        except:
            # Let werkzeug handle the exception
            if debug:
                raise
            
            # Log error and return error page
            log.exception("Exception in %s with params %s", endpt, repr(params))
            return error(request = request)

    return dispatch
