#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-
import env

env.setup()

import time
import wsgiserver
from threading import Thread

from app.wsgiapp import Main

def main():
    webapp = Main(debug=False)

    bind_address = "0.0.0.0"
    app_port = 80

    webapp = wsgiserver.CherryPyWSGIServer((bind_address, app_port), webapp)

    t = Thread(target=webapp.start)
    t.daemon = True
    t.start()

    try:
        while True:
            # Do nothing
            time.sleep(10000)
    except KeyboardInterrupt:
        webapp.stop()

if __name__ == "__main__":
    main()
