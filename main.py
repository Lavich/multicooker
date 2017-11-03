import gc
import uasyncio as asyncio
import sys

from app import app
import hardware
import views


def main(**params):
    gc.collect()
    import logging
    logging.basicConfig(level=logging.INFO)
    gc.collect()

    import micropython
    micropython.mem_info()


    app.init()
    app.debug = True    
    print("* Running on http://%s:%s/" % (app.host, app.port))

    loop = asyncio.get_event_loop()
    loop.create_task(asyncio.start_server(app._handle, app.host, app.port))
    loop.create_task(hardware.run())
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()