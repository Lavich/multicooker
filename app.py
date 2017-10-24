import picoweb
#from . import models
import models

class DBApp(picoweb.WebApp):

    def init(self):
        models.db1.connect()
        models.db2.connect()
        models.Recipe.create_table(True)
        models.Step.create_table(True)
        super().init()

app = DBApp('__main__')
