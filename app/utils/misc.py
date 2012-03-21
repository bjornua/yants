# -*- coding: utf-8 -*-
import json
import os.path
import xml.sax.saxutils

import werkzeug
import werkzeug.routing
import werkzeug.utils
import mako.lookup

import app.widget
import app.config
import pprint

import sqlite3

import xapian
import threading
import contextlib


config = app.config.get()

path = {}
path["static"] = "static"
path["templates"] = "templates"

local = werkzeug.Local()
local_manager = werkzeug.LocalManager([local])
application = local("application")

_sqlitedb = None
def sqlitedb():
    global _sqlitedb
    if _sqlitedb is None:
        new = not os.path.exists("devdb.sqlite3")
        _sqlitedb = sqlite3.connect("devdb.sqlite3", check_same_thread=False)
        _sqlitedb.execute("PRAGMA synchronous=OFF")
        _sqlitedb.execute("PRAGMA journal_mode=OFF")
        _sqlitedb.isolation_level = None
        if new:
            with open("createdatabase.sql") as f: _sqlitedb.executescript(f.read())
    return _sqlitedb

_xapdb = None
xapdb_lock = threading.RLock()
@contextlib.contextmanager
def xapdb():
    with xapdb_lock:
        global _xapdb
        if _xapdb is None:
            new = not os.path.exists("devdb.xapian")
            _xapdb = xapian.WritableDatabase("devdb.xapian", xapian.DB_CREATE_OR_OPEN)
        yield _xapdb

template_lookup = mako.lookup.TemplateLookup(
    directories=[path["templates"]],
    input_encoding="utf-8",
    output_encoding="utf-8",
    strict_undefined=True,
    module_directory="/tmp/mako_modules",
)

def urlfor(endpoint, method=None, _external=False, **values):
    return local.url_adapter.build(endpoint, values, method=method, force_external=_external)

def template_response(templatename, **kwargs):
    kwargs["response"] = local.response
    local.response.data = template_render(templatename, **kwargs)

def template_render(templatename, **kwargs):
    template = template_lookup.get_template(templatename)
    kwargs.update({
        "urlfor": urlfor,
        "escattr": xml.sax.saxutils.quoteattr,
        "escape": xml.sax.saxutils.escape,
        "json": json.dumps,
        "endpoint": local.endpt,
        "endpoint_override": None,
        "widget": app.widget
    })
    return template.render(**kwargs).decode("utf-8")

def redirect(endpoint, *args, **kwargs):
    local.response = werkzeug.utils.redirect(urlfor(endpoint, *args, **kwargs))

def debug(*args, **kwargs):
    local.response.headers["Content-Type"] = "text/plain; charset=UTF-8"
    local.response.data = pprint.pformat(args) + "\n\n" + pprint.pformat(kwargs)
