import gc
import picoweb
import models

class DBApp(picoweb.WebApp):

    def init(self):
        models.db1.connect()
        models.db2.connect()
        models.Recipe.create_table(True)
        models.Step.create_table(True)
        super().init()

    def my_run(self, debug=False, lazy_init=False):
    	gc.collect()
        self.debug = int(debug)
        self.init()
        if not lazy_init:
            for app in self.mounts:
                app.init()


app = DBApp('__main__')
