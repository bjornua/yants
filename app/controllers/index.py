# -*- coding: utf-8 -*-
import werkzeug
from app.utils.misc import templateresponse
import logging

log = logging.getLogger(__name__)

def index(request):
    return templateresponse("/page/main_view.mako")
