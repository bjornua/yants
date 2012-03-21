# -*- coding: utf-8 -*-
import datetime
import uuid
import re
import xapian
import logging

log = logging.getLogger(__name__)

def xapian_makedoc(content):
    doc = xapian.Document()
    indexer = xapian.TermGenerator()
    indexer.set_document(doc)
    indexer.index_text(content)
    return doc

def xapian_create(xapdb, content):
    with xapdb() as xap:
        id_ = xap.add_document(xapian_makedoc(content))
    return id_

def xapian_update(db, xapdb, id_, content):
    id_ = get_xapid(db, id_)
    
    with xapdb() as xap:
        xap.replace_document(id_, xapian_makedoc(content))

def xapian_delete(db, xapdb, id_):
    id_ = get_xapid(db, id_)
    with xapdb() as xap:
        xap.delete_document(id_)

def get_xapid(db, id_):
    sql = 'SELECT "xapian_id" FROM "document" WHERE "id" = ?'
    for value, in db.execute(sql, (id_,)):
        return value

def getsetting(db, key):
    sql = 'SELECT "value" FROM "settings" WHERE "key" = ?'
    for value, in db.execute(sql, (key,)):
        return value
    
def setsetting(db, key, value):
    sql = 'UPDATE "settings" SET "value" = ? WHERE "key" = ?'
    if db.execute(sql, (value,key)).rowcount <= 0:
        sql = 'INSERT INTO "settings"("key","value") VALUES(?,?)'
        db.execute(sql, (key,value))

def popseqid(db):
    db.execute('BEGIN EXCLUSIVE')
    seqid = getsetting(db, "last_seqid")
    if seqid is None:
        seqid = 1
    else:
        seqid = int(seqid) + 1
    setsetting(db, "last_seqid", unicode(seqid))
    db.execute('END')

    return seqid

def nowstamp():
    return datetime.datetime.utcnow().isoformat() + "Z"

def getpeerid(db):
    id_ = getsetting(db, "peer_id")
    
    if id_ is not None:
        return id_
    
    id_ = unicode(uuid.uuid4())

    setsetting(db, "peer_id", id_)
    return id_
        
def create(db, xapdb, content):
    id_ = unicode(uuid.uuid4())
    mtime = nowstamp()
    peerid = getpeerid(db)
    seqid = popseqid(db)
    
    snippet = " ".join(content.split())
    
    if len(snippet) > 16:
        snippet = snippet[0:13].strip() + "..."
    
    xap_id = xapian_create(xapdb, content)
    
    db.execute("""
        INSERT INTO "document" (
            "id", "snippet", "peer_id", "seq_id", "mtime", "content",
            "xapian_id", "deleted")
        VALUES(
            ?, ?, ?, ?, ?, ?, ?, 0
        )
    """, (id_, snippet, peerid, seqid, mtime, content, xap_id))

    return id_, mtime

def update(db, xapdb, id_, content):
    mtime = nowstamp()
    peerid = getpeerid(db)
    seqid = popseqid(db)
    
    snippet = " ".join(content.split())

    if len(snippet) > 16:
        snippet = snippet[0:13].strip() + "..."
    
    sql = """
        UPDATE "document" SET
            "peer_id" = ?,
            "seq_id" = ?,
            "mtime" = ?,
            "snippet" = ?,
            "content" = ?
        WHERE "id" = ?
    """
    if db.execute(sql, (peerid, seqid, mtime, snippet, content, id_)).rowcount < 1:
        return

    xapian_update(db, xapdb, id_, content)

    return mtime, snippet

def get(db, id_):
    sql = 'SELECT "content", "mtime" FROM "document" WHERE "id" = ?'
    for content, mtime in db.execute(sql, (id_,)):
        return mtime, content

def latest(db):
    sql = u'SELECT "id", "content", "mtime" FROM "document" WHERE "deleted" = 0 ORDER by mtime desc LIMIT 8'
    for id_, text, mtime in db.execute(sql):
        yield id_, text, mtime

def delete(db, xapdb, id_):
    mtime = nowstamp()
    peerid = getpeerid(db)
    seqid = popseqid(db)
    
    xapian_delete(db, xapdb, id_)

    sql = '''
        UPDATE "document" SET
            "peer_id" = ?,
            "seq_id" = ?,
            "mtime" = ?,
            "content" = NULL,
            "deleted" = 1
        WHERE "id" = ? and "deleted" = 0
    '''
    if db.execute(sql, (peerid, seqid, mtime, id_)).rowcount > 0:
        
        return mtime,

def search(db, xapdb, query):
    parser = xapian.QueryParser()
    parser.set_default_op(xapian.Query.OP_AND)
    flags = xapian.QueryParser.FLAG_PHRASE
    flags |= xapian.QueryParser.FLAG_PARTIAL
    flags |= xapian.QueryParser.FLAG_LOVEHATE

    with xapdb() as xap:
        parser.set_database(xap) # Needed by xapian partial search
        enquire = xapian.Enquire(xap)
        enquire.set_query(parser.parse_query(query, flags))
        matches = enquire.get_mset(0, 9)
        matches = [x.docid for x in matches]
    
    questionmarks = ", ".join(["?"]*len(matches))

    sql = 'SELECT "id", "content", "mtime", "xapian_id" FROM "document" WHERE "xapian_id" IN ({})'
    sql = sql.format(questionmarks)
    
    for id_, content, mtime, xapid in db.execute(sql, matches):
        matches[matches.index(xapid)] = {"date": mtime, "text": content, "id": id_}

    return matches
