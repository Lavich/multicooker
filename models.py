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


class Step:
    """docstring for Step"""
    __db__ = db

    @classmethod
    def next_id(cls):
        last_id = 0
        keys = list(cls.__db__.db.keys())
        if keys:
            last_id = int(keys[-1].decode())
        return str(last_id + 1)

    @classmethod
    def create(cls, value, id=None):
        if not id:
            id = cls.next_id()
        str = ujson.dumps(value)    
        cls.__db__.db[id] = str
        cls.__db__.db.flush()
        return "{}: {}".format(id, str)

    @classmethod
    def update(cls, id, value):
        return cls.create(value, id=id)

    @classmethod
    def filter(cls, **kwargs):
        for v in cls.__db__.db.values():
            if kwargs:
                for key, value in kwargs.items():
                    try:
                        row = v.decode()
                        row = ujson.loads(row)
                    except:
                        row = {}
                    if type(row) == dict and row.get(key) == value:    
                        yield v.decode()
            else:
                yield v.decode()

    @classmethod
    def get_list(cls, elem):
        for v in cls.__db__.db.values():
            try:
                row = v.decode()
                row = ujson.loads(row)
            except:
                row = {}
            if type(row) == dict and row.get(elem):    
                        yield v.decode()


        