# -*- coding: utf-8 -*-
import logging

from app.controllers.error import notfound
from app.db import notedb, xapdb
from app.helpers import templateresponse, jsonresponse, redirect
from app.mapping import mapto

import app.model.document as document

log = logging.getLogger(__name__)

@mapto("GET", "/")
def index(session, **kwargs):
    counter = int(session.get("counter", 0))
    counter += 1
    session.set("counter", unicode(counter))

    return templateresponse("/page/main_view.mako", counter=counter)

@mapto("GET", "/create")
def create(**kwargs):
    return templateresponse("/page/creator.mako")

@mapto("POST", "/create")
def create_do(request, **kwargs):
    content = request.form.get("content", "")
    document.create(notedb(), xapdb, content)
    return redirect("document.index")

@mapto("GET", "/note/<string:id_>")
def edit(id_, **kwargs):
    doc = document.get(notedb(), id_)
    if doc is None:
        return notfound()
    
    return templateresponse("/page/editor.mako", 
        id_=id_,
        content=doc[1])

@mapto("POST", "/note/<string:id_>")
def edit_do(request, id_, **kwargs):
    content = request.form.get("content", "")
    action = request.form.get("action", "")
    action = action.lower()

    if action == "delete":
        deldata = document.delete(notedb(), xapdb, id_)
        if deldata is None:
            return notfound()
    else:
        updatedata = document.update(notedb(), xapdb, id_, content)
        if updatedata is None:
            return notfound()

    return redirect("document.index")

@mapto("GET", "/sys/search")
def search(request, **kwargs):
    query = request.args.get("q", "")
    result = document.search(notedb(), xapdb, query)
    return jsonresponse(result)

@mapto("GET", "/sys/latest")
def latest(**kwargs):
    docs = document.latest(notedb())
    return jsonresponse([{
        "id": doc[0],
        "text": doc[1],
        "date": doc[2]
    } for doc in docs], indent=4)
