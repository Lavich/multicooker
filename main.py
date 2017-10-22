from app import app
import gc
import views

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
    app.run(debug=True, **params)

    #app.run(debug=True, host='192.168.43.53', port=80, **params)

if __name__ == '__main__':
    main()