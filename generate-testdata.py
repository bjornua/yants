# -*- coding: utf-8 -*-
import env
from pprint import pprint as p
import app.model.document as document
import app.utils.misc
import bz2

import random

xapdb = app.utils.misc.xapdb
db = app.utils.misc.sqlitedb()

wordfile = bz2.BZ2File("wordlist.bz2", "r")
words = wordfile.read()
wordfile.close()

words = words.decode("utf8")
words = words.split("\n")
words = (w.strip() for w in words)
words = (w for w in words if len(w) != 0)
words = list(words)


doccount = 10000
for i in range(doccount):
    print "{:3d}% | Creating doc {} of {}".format((i*100)//doccount, i+1, doccount)

    w = list()
    for _ in range(random.randint(1,1000)):
        w.append(random.choice(words))
    
    content = " ".join(w)

    document.create(db, xapdb, content)
