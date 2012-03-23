# -*- coding: utf-8 -*-
import json
import os.path
import xml.sax.saxutils

import mako.lookup
import werkzeug
import werkzeug.utils

template_lookup = mako.lookup.TemplateLookup(
    directories=["templates"],
    input_encoding="utf-8",
    output_encoding="utf-8",
    strict_undefined=True,
    module_directory="/tmp/mako_modules",
)

def runtemplate(templatename, response, **kwargs):
    kwargs["response"] = response
    response.data = rendertemplate(templatename, **kwargs)

def rendertemplate(templatename, **kwargs):
    template = template_lookup.get_template(templatename)
    kwargs.update({
        "urlfor": app.mapping.urlfor,
        "escattr": xml.sax.saxutils.quoteattr,
        "escape": xml.sax.saxutils.escape,
        "json": json.dumps,
        "widget": app.widget
    })
    return template.render(**kwargs).decode("utf-8")

import app.mapping
import app.widget
