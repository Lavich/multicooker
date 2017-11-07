import gc
import uasyncio as asyncio
import sys

from app import app
import views


def main(**params):
    gc.collect()
    import logging
    logging.basicConfig(level=logging.INFO)
    gc.collect()

    import micropython
    micropython.mem_info()

    app.run(debug=True)


if __name__ == '__main__':
    main()