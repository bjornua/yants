# -*- coding: utf-8 -*-
import logging
import random
from datetime import datetime, timedelta

log = logging.getLogger(__name__)


class Session(object):
    def __init__(self, db, id_, token, ttl=600):
        self.db = db
        
        if id_ is None or token is None or not dbexists(db, id_, token, ttl):
            self.id = None
            self.token = None
            return
        
        self.id = id_
        self.token = token

        dbtouch(self.db, self.id) 

    def get(self, key, default=None):
        if self.id is None:
            return default

        data = dbget(self.db, self.id, key)
        if data is None:
            return default

        return data

    def set(self, key, value):
        if self.id is None:
            self.token = generatetoken()
            self.id = dbcreate(self.db, self.token)

        dbset(self.db, self.id, key, value)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def generatetoken():
    return "".join(random.choice(alphabet) for _ in range(64))

# Formats timestamp for use in database (assumes all dates are UTC)
def timestamp(date):
    return date.replace(microsecond=0).isoformat() + "Z"

def dbexists(db, id_, token, ttl):
    sql = 'SELECT "token","last_touch" FROM "sessions" WHERE "id" = ?'
    row = db().execute(sql, (id_,)).fetchone()
    
    if row is None:
        return False
    
    expirydate = timestamp(datetime.utcnow() - timedelta(seconds=ttl))
    
    return token == row[0] and expirydate < row[1]

def dbcreate(db, token):
    now = timestamp(datetime.utcnow())
    sql = 'INSERT INTO "sessions"("token", "last_touch") VALUES(?,?)'
    return db().execute(sql, (token,now)).lastrowid

def dbtouch(db, id_):
    now = timestamp(datetime.utcnow())
    sql = 'UPDATE "sessions" SET "last_touch" = ? WHERE "id" = ?'
    db().execute(sql, (now, id_))

def dbcleanup(db, ttl):
    expirydate = timestamp(datetime.utcnow() - timedelta(seconds=ttl))
    sql = 'DELETE FROM "sessions" WHERE "last_touch" < ?'
    db().execute(sql, (expirydate,))

def dbget(db, id_, key):
    sql = 'SELECT "value" FROM "session_data" WHERE "session_id" = ? AND "key" = ?'
    for value, in db().execute(sql, (id_, key)):
        return value

def dbset(db, id_, key, value):
    sql = 'UPDATE "session_data" SET "value" = ? WHERE "session_id" = ? AND "key" = ?'
    if db().execute(sql, (value, id_, key)).rowcount >= 1:
        return

    sql = 'INSERT INTO "session_data"("session_id","key","value") VALUES(?,?,?)'
    db().execute(sql, (id_, key, value))
