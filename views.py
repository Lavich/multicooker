#from .app import app
#from .models import Recipe, Step
from app import app
from models import Step

import ure as re
import picoweb


def generate_url(name):
    return 'http://' + app.host + '/' + str(app.port) + name.replace(" ", "-")


@app.route('/')
def index(request, response):
    yield from app.sendfile(response, 'templates/index.html')


@app.route('/api/recipes')
def recipe_list(request, response):
    """
    Get list recipes
    """
    recipe_names = list(set(list(Step.filter('recipe_name'))))
    recipe_list = list(map(lambda x: {'name': x, 'url':  generate_url('/api/steps/' + x)}, recipe_names))
    yield from picoweb.jsonify(response, {'recipes': recipe_list})


@app.route(re.compile('^/api/recipes/(.+)'))
def recipe_detail(request, response):
    """
    Get detail recipe[recipe_name]
    """
    pkey = picoweb.utils.unquote_plus(request.url_match.group(1))
    pkey = pkey.replace("-", " ")
    steps = list(Step.filter(recipe_name=pkey))
    print(steps)
    yield from picoweb.jsonify(response, {'steps': steps})


@app.route('/api/steps', methods=['POST'])
def step_list(request, response):
    if request.method == 'POST':
        """
        Create new Step
        """
        yield from request.read_form_data()
        data = request.form
        for key in data.keys():
            data[key] = data[key][0]
        print(data)
        if data.get('recipe_name'):
            new_step = Step.create(data)
            print(new_step)
            yield from picoweb.jsonify(response, {'step': new_step})


@app.route(re.compile('^/api/steps/(.+)'), methods=['PUT', 'DELETE'])
def step_detail(request, response):
    pkey = picoweb.utils.unquote_plus(request.url_match.group(1))
    if request.method == 'PUT':
        """
        Update Step[id]
        """
        yield from request.read_form_data()
        data = request.form
        print(data)
        for key in data.keys():
            data[key] = data[key][0]
        step = Step.update(pkey, data)
        print(step)
        yield from picoweb.jsonify(response, {'step': step})

    if request.method == 'DELETE':
        """
        Delete Step[id]
        """
        Step.delete(pkey)
        yield from picoweb.jsonify(response, {'success': 'True'})
