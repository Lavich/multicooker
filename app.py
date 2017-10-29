import gc
import picoweb
import models


class DBApp(picoweb.WebApp):

    def init(self):
        models.db.connect()
        super().init()


app = DBApp('__main__')
