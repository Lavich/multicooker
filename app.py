import gc
import picoweb
import sys
import uasyncio as asyncio
import models
from hardware import sensor, timer_event, heater


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

    def run(self, debug=False, lazy_init=False):
        gc.collect()
        self.debug = int(debug)
        self.init()
        if not lazy_init:
            for app in self.mounts:
                app.init()
        loop = asyncio.get_event_loop()
        if debug:
            print("* Running on http://%s:%s/" % (self.host, self.port))
        loop.create_task(asyncio.start_server(self._handle, self.host, self.port))
        loop.create_task(sensor())
        loop.create_task(heater(timer_event))
        loop.run_forever()
        loop.close()


app = DBApp('__main__')
