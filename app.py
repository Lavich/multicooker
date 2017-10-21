import picoweb
#from . import models
import models

class DBApp(picoweb.WebApp):

    def init(self):
        models.db.connect()
        models.Recept.create_table(True)
        models.Step.create_table(True)
        super().init()

app = DBApp('__main__')
