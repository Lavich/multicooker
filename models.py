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
    def public(cls):
        print("public")
        for v in cls.__db__.db.values():
            res = ujson.loads(v)
            row = cls.Row(*res)
            if row.archived:
                continue
            yield row

    @classmethod
    def json(cls):
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
        print("public")
        for v in cls.__db__.db.values():
            res = ujson.loads(v)
            row = cls.Row(*res)
            if row.recipe_id == recipe_id and not row.archived:
                yield row
            
