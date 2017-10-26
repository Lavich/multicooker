from ucollections import OrderedDict
import ujson
import utime

import btreedb as uorm
import btree


db1 = uorm.DB("recipe.db")
db2 = uorm.DB("step.db")


class Recipe(uorm.Model):

    __db__ = db1
    __table__ = "recipe"
    __schema__ = OrderedDict([
        ("id", ("INT", 0)),
        ("archived", ("INT", 0)),
        ("name", ("TEXT", "")),
        ("description", ("TEXT", "")),
    ])

    @classmethod
    def auto_inc_field(cls):
        b = list(cls.__db__.db.keys())[-1]
        return int(b.decode()) + 1

    @classmethod
    def get_id(cls, pkey):
        try:
            int(pkey)
        except:
            return
        keys = cls.__schema__.keys()
        row = cls.Row(*ujson.loads(cls.__db__.db[pkey]))
        d = dict()
        for key, value in zip(keys, row):
            d[key] = value
        return d

    @classmethod
    def all(cls):
        print("json")
        keys = cls.__schema__.keys()
        for v in cls.__db__.db.values():
            res = ujson.loads(v)
            row = cls.Row(*res)
            if row.archived:
                continue
            d = dict()
            for key, value in zip(keys, row):
                d[key] = value
            yield d


class Step(uorm.Model):

    __db__ = db2
    __table__ = "step"
    __schema__ = OrderedDict([
        ("id", ("INT", 0)),
        ("recipe_id", ("INT", 0)),
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
    def filter_on_recipe(cls, recipe_id):
        keys = cls.__schema__.keys()
        for v in cls.__db__.db.values():
            res = ujson.loads(v)
            row = cls.Row(*res)
            if row.archived:
                yield row
            if row.recipe_id == recipe_id:
                d = dict()
                for key, value in zip(keys, row):
                    d[key] = value
                yield d
