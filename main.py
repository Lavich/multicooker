import gc
import uasyncio as asyncio

from app import app
import views

host="127.0.0.1"
port=8081


async def toggle():
    while True:
        await asyncio.sleep_ms(1000)
        print(42)


def main(**params):
    gc.collect()
    import logging
    logging.basicConfig(level=logging.INFO)

    # Preload templates to avoid memory fragmentation issues
    gc.collect()
    app._load_template('index.html')
    #app._load_template('note.html')
    gc.collect()

    import micropython
    micropython.mem_info()
   # app.run(debug=True, **params)
    #app.run(debug=True, host='192.168.43.53', port=80, **params)

    app.my_run(debug=True)
    
    loop = asyncio.get_event_loop()
    if app.debug:
            print("* Running on http://%s:%s/" % (host, port))
    loop.create_task(asyncio.start_server(app._handle, host, port))
    loop.create_task(toggle())
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()