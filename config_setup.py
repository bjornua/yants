#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-
import env
import os.path
import sys
import app.config
from pprint import pprint

def user_query(itemname, converter, defaultrep, default=None):
    while True:
        if default == None:
            answer = raw_input("Indtast %s: " % (itemname,))
        else:
            answer = raw_input("Indtast %s [%s]: " % (itemname, defaultrep(default)))
            if answer == "":
                return default
        try:
            answer = converter(answer)
        except:
            print "Kunne ikke forstå værdien, prøv igen."
            continue
        return answer

def prompt_update_config():
    config = app.config.get()

    for name, key, converter, repr_ in [
        ("CouchDB Server URL", "couchdb_server_url", str, str),
        ("CouchDB db", "couchdb_db", str, str),
    ]:
        config[key] = user_query(name, converter, repr_, config[key])
    return config

def write_config(config):
    filename = os.path.join("app", "config", "user.py")
    with open(filename, "w") as f:
        print >> f, "# -*- coding: utf-8 -*-"
        print >> f, "from app.config.default import config"
        print >> f, "config = \\"
        pprint(config, f, indent=4, width=1)

def main():
    config = prompt_update_config()
    write_config(config)

if __name__ == "__main__":
    main()
