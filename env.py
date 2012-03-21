# -*- coding: utf-8 -*-
import sys
import os.path as path
import os
import logging

dname = path.realpath(path.dirname(__file__))
extlib = path.join(dname, "extlib")

sys.path[0] = dname

# Prepend 3rd-party libraries to path
sys.path.insert(0, extlib)

os.chdir(dname)


logfmt = "%(name)s:%(lineno)4d:%(levelname)8s: %(message)s"
logging.basicConfig(format=logfmt, level=logging.DEBUG)
