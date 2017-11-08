from app import app
from models import Recipe
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
        timer_event.set(60 * int(data.get('time')[0]))
        setpoint_event.set(int(data.get('temp')[0]))
        
        yield from picoweb.jsonify(response, {'success': 'True'})


@app.route('/stop')
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

    if temp_event.is_set():
        data['temperature'] = round(temp_event.value(), 1)
    if timer_event.is_set():
        data['time_lost'] = round(timer_event.value()/60, 2)
    if setpoint_event.is_set():
        data['setpoint'] = round(setpoint_event.value(), 1)
    data['u'] = round(mypid.output, 1)
    data['p'] = mypid.Kp
    data['i'] = mypid.Ki
    data['d'] = mypid.Kd
    yield from picoweb.jsonify(response, data)
