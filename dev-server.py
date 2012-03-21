#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-
import env

from werkzeug import run_simple
from app.wsgiapp import Main

def main():
    app = Main(debug=True)
    bind_address = "127.0.0.1"
    port = 5000
    run_simple(
        bind_address, port, app, use_debugger=True, use_reloader=True
    )

if __name__ == "__main__":
    main()
