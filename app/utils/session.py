# -*- coding: utf-8 -*-
from app.utils.misc import db
import app.utils.date as dateutils

class InvalidCookie(Exception): pass

class Session(object):
    def __init__(self, id_, expires):
        self.id = id_
        self.is_init = False
        self.expires = expires
    
    def init(self):
        if self.is_init:
            return
        self.is_init = True

        self.date = dateutils.now()
        if self.id != None:
            try:
                self.load_session()
                return
            except InvalidCookie:
                pass
        self.new_session()
    
    def get_doc(self, id_):
        for result in db().view("session/by_id", key=id_, include_docs=True):
            return result["doc"]

    def load_session(self):
        doc = self.get_doc(self.id)

        if doc is None:
            raise InvalidCookie()

        # Expire time on session
        if (dateutils.now() - dateutils.fromtuple(doc["date"])).total_seconds() > self.expires:
            raise InvalidCookie()
        
        doc["date"] = dateutils.totuple(self.date)
        self.doc = doc
        
    def new_session(self):
        self.doc = {"type": "session", "data":{}, "date": dateutils.totuple(self.date)}
    
    def save(self):
        if self.is_init:
            db().save_doc(self.doc)
            self.id = self.doc["_id"]
    
    def get(self, *args, **kwargs):
        self.init()
        return self.doc["data"].get(*args,**kwargs)
    
    def __setitem__(self, *args, **kwargs):
        self.init()
        return self.doc["data"].__setitem__(*args,**kwargs)
    
    def set_cookie(self, response):
        if self.is_init:
            response.set_cookie("session", self.id, max_age=31536000)
