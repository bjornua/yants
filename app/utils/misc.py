# -*- coding: utf-8 -*-
import contextlib
import json
import os.path
import sqlite3
import threading
import xml.sax.saxutils

import mako.lookup
import werkzeug
import werkzeug.utils
import xapian

import app.mapping
import app.widget


def sqlitedb_lazy():
    db = None
    def getter():
        if db is not None:
            new = not os.path.exists("devdb.sqlite3")
            db = sqlite3.connect("devdb.sqlite3", check_same_thread=False)
            db.execute("PRAGMA synchronous=OFF")
            db.execute("PRAGMA journal_mode=OFF")
            db.isolation_level = None
            if new:
                with open("createdatabase.sql") as f:
                    db.executescript(f.read())
        return db
    return getter

sqlitedb = sqlitedb_lazy()

def xapdb_lazy():
    db = None
    lock = threading.RLock()
    @contextlib.contextmanager
    def getter():
        with lock:
            if db is None:
                db = xapian.WritableDatabase("devdb.xapian", xapian.DB_CREATE_OR_OPEN)
            yield db

xapdb = xapdb_lazy()

template_lookup = mako.lookup.TemplateLookup(
    directories=["templates"],
    input_encoding="utf-8",
    output_encoding="utf-8",
    strict_undefined=True,
    module_directory="/tmp/mako_modules",
)

def urlfor(endpoint, method=None, _external=False, **values):
    return app.mapping.url_adapter.build(endpoint, values, method=method, force_external=_external)

def templateresponse(templatename, **kwargs):
    response = werkzeug.Response()
    runtemplate(templatename, response, **kwargs)
    return response

def runtemplate(templatename, response, **kwargs):
    kwargs["response"] = response
    response.data = rendertemplate(templatename, **kwargs)

def rendertemplate(templatename, **kwargs):
    template = template_lookup.get_template(templatename)
    kwargs.update({
        "urlfor": urlfor,
        "escattr": xml.sax.saxutils.quoteattr,
        "escape": xml.sax.saxutils.escape,
        "json": json.dumps,
        "widget": app.widget
    })
    return template.render(**kwargs).decode("utf-8")

def redirect(endpoint, *args, **kwargs):
    return werkzeug.utils.redirect(urlfor(endpoint, *args, **kwargs))
