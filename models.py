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
    def create(cls, data, id=None):
        if not id:
            id = cls.next_id()
        str = ujson.dumps(data)    
        cls.__db__.db[id] = str
        cls.__db__.db.flush()
        return "{}: {}".format(id, str)

    @classmethod
    def update(cls, id, value):
        return cls.create(value, id=id)

    @classmethod
    def filter(cls, *args, **kwargs):
        """
        >>> filter('recipe_name')
        ['Pasta', 'Tea', 'Cake']

        >>> filter(recipe_name='Pasta')
        {'id': '7', temp': '100', 'time': '8', 'recipe_name': 'Pasta'}
        """
        if args:
            elem = str(args[0])
            for v in cls.__db__.db.values():
                try:
                    row = v.decode()
                    row = ujson.loads(row)
                except:
                    row = {}
                if type(row) == dict and row.get(elem):    
                    yield row.get(elem)

        elif kwargs:
            for k, v in cls.__db__.db.items():
                for key, value in kwargs.items():
                    try:
                        row = v.decode()
                        row = ujson.loads(row)
                    except:
                        row = {}
                    if type(row) == dict and row.get(key) == value:    
                        step = ujson.loads(v.decode())
                        step['id'] = k.decode()
                        yield step
        else:
            for value in cls.__db__.db.values():
                yield value.decode()

        