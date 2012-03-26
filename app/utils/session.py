# -*- coding: utf-8 -*-
import random
from datetime import datetime, timedelta

import app.utils.date as dateutils

import logging

log = logging.getLogger(__name__)

alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
def generate_token():
    return "".join(random.choice(alphabet) for _ in range(64))

# Formats timestamp for use in database (assumes all dates are UTC)
def timestamp(date):
    return date.replace(microsecond=0).isoformat() + "Z"

class Session(object):
    def __init__(self, db, id_, token, ttl=600):
        self.db = db
        
        if id_ is None or token is None or not verify_session(db, id_, token, ttl):
            self.id = None
            self.token = None
            return
        
        self.id = id_
        self.token = token

        touch_session(self.id) 

    def get(self, key, default=None):
        if self.id is None:
            log.debug("Returning default %s", repr(default))
            return default

        data = session_get(self.db, self.id, key)
        if data is None:
            return default

        return data

    def set(self, key, value):
        if self.id is None:
            self.token = generate_token()
            self.id = create_session(self.db, self.token)

        session_set(self.db, self.id, key, value)

def verify_session(db, id_, token, ttl):
    sql = 'SELECT "token","last_touch" FROM "sessions" WHERE "id" = ?'
    row = db.execute(sql, (id_,)).fetchone()
    
    if row is None:
        return False
    
    expirydate = timestamp(datetime.utcnow() - timedelta(seconds=ttl))
    dbtoken, last_touch = row
    
    if token != dbtoken:
        return False
    
    if last_touch < expirydate:
        return False

    return True

def create_session(db, token):
    now = timestamp(datetime.utcnow())
    sql = 'INSERT INTO "sessions"("token", "last_touch") VALUES(?,?)'
    return db.execute(sql, (token,now)).lastrowid

def update_time(db, id):
    now = timestamp(datetime.utcnow())
    sql = 'UPDATE "sessions" SET "last_touch" = ? WHERE "id" = ?'
    db.execute(sql, (now, id_))

def session_cleanup(db, ttl):
    expirydate = timestamp(datetime.utcnow() - timedelta(seconds=ttl))
    sql = 'DELETE FROM "sessions" WHERE "last_touch" < ?'
    db.execute(sql, (expirydate,))

def session_get(db, id_, key):
    log.debug("Calling session_get with %s %s %s", repr(db), repr(id_), repr(key))
    sql = 'SELECT "value" FROM "session_data" WHERE "session_id" = ? AND "key" = ?'
    for value, in db.execute(sql, (id_, key)):
        return value

def session_set(db, id_, key, value):
    sql = 'UPDATE "session_data" SET "value" = ? WHERE "session_id" = ? AND "key" = ?'
    if db.execute(sql, (value, id_, key)).rowcount >= 1:
        return

    sql = 'INSERT INTO "session_data"("session_id","key","value") VALUES(?,?,?)'
    db.execute(sql, (id_, key, value))
