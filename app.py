import gc
import picoweb
import sys

import models


class DBApp(picoweb.WebApp):

    def init(self):
        models.db.connect()
        super().init()
        app.debug = False     
    	
    	print(sys.platform)
    	if sys.platform == 'linux':
    		self.host="127.0.0.1"
    		self.port=8081
    	else:
    		self.host='192.168.43.53'
	        self.port=80



app = DBApp('__main__')
