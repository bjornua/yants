# -*- coding: utf-8 -*-
import contextlib
import os
import os.path as path
import sqlite3
import threading
import xapian


createsql = """
    CREATE TABLE "document"(
        "id" TEXT,
        "peer_id" TEXT,
        "seq_id" INTEGER,
        "mtime" TEXT, 
        "content" TEXT,
        "xapian_id" INTEGER,
        "snippet" TEXT,
        "deleted" INTEGER
    );

    CREATE UNIQUE INDEX "idx_id"          ON "document" ("id" ASC);
    CREATE UNIQUE INDEX "idx_xapian_id"   ON "document" ("xapian_id" ASC);
    CREATE UNIQUE INDEX "idx_replication" ON "document" ("peer_id" ASC, "seq_id" ASC);
    CREATE INDEX        "idx_latest"      ON "document" ("deleted" ASC, "mtime" DESC);

    CREATE TABLE "settings"("key" TEXT, "value" TEXT);
    CREATE UNIQUE INDEX "idx_key"         ON "settings" ("key" ASC);
"""

def preparedatadir():
    if not path.isdir("data"):
        os.mkdir("data")

def sqlitedb_lazy():
    db = [None]
    def getter():
        if db[0] is None:
            preparedatadir()
            new = not path.exists("data/notes")
            db[0] = sqlite3.connect("data/notes", check_same_thread=False)
            db[0].execute("PRAGMA synchronous=OFF")
            db[0].execute("PRAGMA journal_mode=OFF")
            db[0].isolation_level = None
            if new:
                db[0].executescript(createsql)
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
                preparedatadir()
                db[0] = xapian.WritableDatabase("data/search", xapian.DB_CREATE_OR_OPEN)
            yield db[0]
    
    return getter
xapdb = xapdb_lazy()
