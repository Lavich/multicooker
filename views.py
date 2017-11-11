from app import app
from models import Recipe
import math
import ure as re
import picoweb
from hardware import timer_event, mypid, setpoint_event, temp_event


@app.route('/')
def index(request, response):
    yield from app.sendfile(response, 'templates/index.html')


@app.route('/recipes')
def recipe_list(request, response):
    """
    Get list recipes
    """
    if request.method == 'GET':
        recipe_list = list(Recipe.get_all_recipes())
        print(recipe_list)
        yield from picoweb.jsonify(response, recipe_list)

    if request.method == 'POST':
        yield from request.read_form_data()
        data = request.form
        for key in data.keys():
            data[key] = data[key][0]
        print(data)
        clear_data = {}
        for name in Recipe.fields:
            clear_data[name] = data.get(name)
        if clear_data['name'] and clear_data['time'] and clear_data['temp']:
            new_recipe = Recipe.create(clear_data, id=clear_data.get(name))
            print(new_recipe)
            yield from picoweb.jsonify(response, {'success': 'True'})


@app.route(re.compile('^/recipes/(.+)'))
def recipe_detail(request, response):
    """
    Delete recipe
    """
    if request.method == 'DELETE':
        Recipe.delete(pkey)
        yield from picoweb.jsonify(response, {'success': 'True'})


@app.route(re.compile('^/start'))
def start(request, response):
    """
    Start heating
    request = {'time': 10, 'temp': 100}
    """
    if request.method == 'POST':
        yield from request.read_form_data()
        data = request.form
        print(data)
        timer_event.set(60 * int(data.get('time_set')[0]))
        setpoint_event.set(int(data.get('temp_set')[0]))
        
        yield from picoweb.jsonify(response, {'success': 'True'})


@app.route('/stop', method = 'POST')
def stop(request, response):
    """
    Stop heating
    """
    timer_event.clear()
    yield from picoweb.jsonify(response, {'success': 'True'})


@app.route('/status')
def status(request, response):
    """
    Return status
    """
    data = {}
    if setpoint_event.is_set():
        data['temp_set'] = round(setpoint_event.value())
    if temp_event.is_set():
        data['temp_now'] = round(temp_event.value(), 1)
    if timer_event.is_set():
        data['time_left'] = math.ceil(timer_event.value() / 60)
        data['is_start'] = True
    else:
        data['is_start'] = False
    yield from picoweb.jsonify(response, data)


@app.route('/pid')
def pid(request, response):
    """
    Return status
    """
    data = {}

    if temp_event.is_set():
        data['temp_now'] = round(temp_event.value())
    if setpoint_event.is_set():
        data['temp_set'] = round(setpoint_event.value())
    data['u'] = round(mypid.output, 1)
    data['p_term'] = round(mypid.PTerm, 1)
    data['i_term'] = round(mypid.ITerm, 1)
    data['d_term'] = round(mypid.DTerm, 1)
    data['p'] = mypid.Kp
    data['i'] = mypid.Ki
    data['d'] = mypid.Kd
    yield from picoweb.jsonify(response, data)


# @app.route('/wifi')
# def wifi(request, response):
#     """
#     Return status
#     """
#     if request.method == 'GET':
#         recipe_list = list(Recipe.get_all_recipes())
#         print(recipe_list)
#         yield from picoweb.jsonify(response, recipe_list)

#     if request.method == 'POST':
#         yield from request.read_form_data()
#         data = request.form
#         for key in data.keys():
#             data[key] = data[key][0]
#         print(data)
#         if data['ssid'] and data['password']:
#             import network
#             sta = network.WLAN(network.STA_IF)
#             sta.active(True)
#             sta.connect(data['ssid'], data['password'])
#             yield from picoweb.jsonify(response, {'success': 'True'})
#         if data['disconnect']:
#             import network
#             ap = network.WLAN(network.AP_IF)
#             ap.active(True)
#             ap.config(essid="network-name", authmode=network.AUTH_WPA_WPA2_PSK, password="abcdabcdabcd")
#             yield from picoweb.jsonify(response, {'success': 'True'})