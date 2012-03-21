# -*- coding: utf-8 -*-
from app.utils.misc import template_response, local, sqlitedb, xapdb, redirect
from app.controllers.error import notfound

import json
import app.model.document as document
import logging

log = logging.getLogger(__name__)

def newdoc():
    template_response("/page/creator.mako")

def newdoc_do():
    content = local.request.form.get("content", "")
    document.create(sqlitedb(), xapdb, content)
    redirect("index")


def edit(id_):
    doc = document.get(sqlitedb(), id_)
    if doc is None:
        return notfound()
    
    template_response("/page/editor.mako", 
        id_=id_,
        content=doc[1])

def edit_do(id_):
    content = local.request.form.get("content", "")
    action = local.request.form.get("action", "")
    action = action.lower()

    if action == "delete":
        deldata = document.delete(sqlitedb(), xapdb, id_)
        if deldata is None:
            return notfound()
                
    else:
        updatedata = document.update(sqlitedb(), xapdb, id_, content)

        if updatedata is None:
            return notfound()

    return redirect("index")

def get(id_):
    doc = document.get(sqlitedb(), id_)
    if doc is None:
        return notfound()
    
    local.response.data = json.dumps({
        "date": doc[0],
        "text": doc[1]
    }, indent=4)


def search():
    query = local.request.args.get("q", "")
    local.response.data = json.dumps(document.search(sqlitedb(), xapdb, query))
    
def latest():
    docs = document.latest(sqlitedb())
    
    local.response.data = json.dumps([{
        "id": doc[0],
        "text": doc[1],
        "date": doc[2]
    } for doc in docs], indent=4)

def create():
    content = local.request.form.get("content", "")
    id_, mtime = document.create(sqlitedb(), xapdb, content)
    
    local.response.data = json.dumps({"id": id_, "mtime": mtime}, indent=4)

def update(id_):
    content = local.request.form.get("content", "")
    
    updatedata = document.update(sqlitedb(), xapdb, id_, content)

    if updatedata is None:
        local.response.status_code = 404
        local.response.data = json.dumps({
            "error": [0, "Document does not exist"]
        })
        return

    mtime, snippet = updatedata
    
    local.response.data = json.dumps({
        "mtime": mtime,
        "snippet": snippet
    })

def delete(id_):
    deldata = document.delete(sqlitedb(), xapdb, id_)

    if deldata is None:
        local.response.status_code = 404
        local.response.data = json.dumps({
            "error": [0, "Document does not exist"]
        })
        return
        
    mtime, = deldata


    local.response.data = json.dumps({
        "mtime": mtime,
    })


#    try:
#        page = int(local.request.args.get("p", ""))
#    except ValueError:
#        page = 0
#    else:
#        page = max(page, 0)

