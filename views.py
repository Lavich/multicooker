from app import app
from models import Recipe
import ure as re
import picoweb
from hardware import timer_event


@app.route('/')
def index(request, response):
    yield from app.sendfile(response, 'index.html')


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
        if data.get('time') and data.get('temp'):
            time = int(data.get('time')[0]) * 60
            setpoint = int(data.get('temp')[0])
            timer_event.set({'time': time, 'setpoint': setpoint})
            print(timer_event.value())
        yield from picoweb.jsonify(response, {'success': 'True'})


@app.route('/stop')
def stop(request, response):
    """
    Stop heating
    """
    timer_event.clear()
    yield from picoweb.jsonify(response, {'success': 'True'})
