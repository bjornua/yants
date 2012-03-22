# -*- coding: utf-8 -*-
import werkzeug.routing

import app.controllers.index
import app.controllers.document
import app.controllers.error

endpts = {
# Normal endpoints
    "index": app.controllers.index.index,
    "docget": app.controllers.document.get,
    "doccreate": app.controllers.document.create,
    "docnewdoc": app.controllers.document.newdoc,
    "docnewdocdo": app.controllers.document.newdoc_do,
    "docupdate": app.controllers.document.update,
    "docsearch": app.controllers.document.search,
    "doclatest": app.controllers.document.latest,
    "docdelete": app.controllers.document.delete,
    "docedit": app.controllers.document.edit,
    "doceditdo": app.controllers.document.edit_do,

# System endpoints
    "notfound": app.controllers.error.notfound,
    "error": app.controllers.error.error,
}

url_map = werkzeug.routing.Map()

for method, path, endpoint in [
        ("DELETE", "/sys/note/<string:id_>", "docdelete"),
        ("GET", "/", "index"),
        ("GET", "/note/<string:id_>", "docedit"),
        ("GET", "/create", "docnewdoc"),
        ("GET", "/sys/latest", "doclatest"),
        ("GET", "/sys/search", "docsearch"),
        ("GET", "/sys/note/<string:id_>", "docget"),
        ("GET", "/sys/note/<string:id_>", "docget"),
        ("POST", "/note/<string:id_>", "doceditdo"),
        ("POST", "/create", "docnewdocdo"),
        ("POST", "/sys/create", "doccreate"),
        ("PUT", "/sys/note/<string:id_>", "docupdate"),
    ]:
    rule = werkzeug.routing.Rule(path, methods=[method], endpoint=endpoint)
    url_map.add(rule)
