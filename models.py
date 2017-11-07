import ujson
import btree


class DB:

    def __init__(self, name, **options):
        self.name = name
        self.f = None
        self.db = None
        self.options = options

    def connect(self):
        try:
            self.f = open(self.name, "r+b")
        except OSError:
            self.f = open(self.name, "w+b")
        self.db = btree.open(self.f, **self.options)

    def close(self):
        self.db.close()
        self.f.close()   


db = DB("multicooker.db")


class Recipe:
    """docstring for Step"""
    __db__ = db
    fields = ['name', 'time', 'temp']

    @classmethod
    def create(cls, data, id='0'): 
        cls.__db__.db[str(id)] = data
        cls.__db__.db.flush()
        return data

    @classmethod
    def delete(cls, key):
        del cls.__db__.db[str(key)]

    @classmethod
    def get_all_recipes(cls, *args, **kwargs):
        for value in cls.__db__.db.values():
            yield ujson.loads(value.decode())
     