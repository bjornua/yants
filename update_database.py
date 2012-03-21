#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-
import env
import couchdbkit
from app.utils.misc import db
from app.utils.folder import get_nodes
import os.path as path

def main():
    views = set()
    for p in get_nodes(["views"]):
        if len(p) != 2:
            continue
        
        p = path.join(*p)

        if not path.isdir(p):
            continue
        
        couchdbkit.designer.push(p, db())

if __name__ == "__main__":
    main()
