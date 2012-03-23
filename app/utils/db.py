# -*- coding: utf-8 -*-
import contextlib
import os.path
import sqlite3
import threading
import xapian

def sqlitedb_lazy():
    db = [None]
    def getter():
        if db[0] is None:
            new = not os.path.exists("devdb.sqlite3")
            db[0] = sqlite3.connect("devdb.sqlite3", check_same_thread=False)
            db[0].execute("PRAGMA synchronous=OFF")
            db[0].execute("PRAGMA journal_mode=OFF")
            db[0].isolation_level = None
            if new:
                with open("createdatabase.sql") as f:
                    db[0].executescript(f.read())
        return db[0]
    return getter

sqlitedb = sqlitedb_lazy()

def xapdb_lazy():
    db = [None]
    lock = threading.RLock()
    @contextlib.contextmanager
    def getter():
        with lock:
            if db[0] is None:
                db[0] = xapian.WritableDatabase("devdb.xapian", xapian.DB_CREATE_OR_OPEN)
            yield db[0]
    
    return getter
xapdb = xapdb_lazy()
