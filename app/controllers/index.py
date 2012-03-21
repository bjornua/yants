# -*- coding: utf-8 -*-
from app.utils.misc import template_response, local, urlfor, redirect
import logging

log = logging.getLogger(__name__)

def index():
    template_response("/page/main_view.mako")
