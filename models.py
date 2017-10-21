from ucollections import OrderedDict
import ujson
import utime

import btreedb as uorm
import btree


db = uorm.DB("notes.db")

class Recept(uorm.Model):

    __db__ = db
    __table__ = "recept"
    __schema__ = OrderedDict([
        ("id", ("INT", 0)),
        ("archived", ("INT", 0)),
        ("name", ("TEXT", "")),
        ("description", ("TEXT", "")),
    ])


    @classmethod
    def public(cls):
        print("public")
        for v in cls.__db__.db.values(None, None, btree.DESC):
            res = ujson.loads(v)
            row = cls.Row(*res)
            if row.archived:
                continue
            yield row


class Step(uorm.Model):

    __db__ = db
    __table__ = "step"
    __schema__ = OrderedDict([
        ("id", ("INT", 0)),
        ("recept_id", ("INT", 0)),
        ("archived", ("INT", 0)),
        ("number", ("INT", 0)),
        ("temperature", ("INT", 100)),
        ("time", ("INT", 10)),
        ("auto", ("INT", 0)),
        ("wait", ("INT", 0)),
        ("bell", ("INT", 0)),
        ("description", ("TEXT", "")),
    ])


    @classmethod
    def public(cls):
        print("public")
        for v in cls.__db__.db.values(None, None, btree.DESC):
            res = ujson.loads(v)
            row = cls.Row(*res)
            if row.archived:
                continue
            yield row
