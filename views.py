#from .app import app
#from .models import Recipe, Step
from app import app
from models import Step

import ure as re
import picoweb
import ijson


def generate_url(name):
    return 'http://' + app.host + '/' + str(app.port) + name


@app.route('/')
def index(request, response):
    yield from app.sendfile(response, 'templates/index.html')


@app.route('/api', methods=['GET'])
def api(request, response):
    api_url = {
        'steps': generate_url('/api/steps'),
        'multicooker': generate_url('/api/multicooker')
    }
    yield from picoweb.jsonify(response, api_url)


@app.route('/api/steps', methods=['GET', 'POST'])
def steps(request, response):
    if request.method == 'GET':
        steps_list = list(set(list(Step.get_list('recipe_name'))))
        steps = list(map(lambda x: {x: generate_url('/api/steps/' + x)}, steps_list))
        yield from picoweb.jsonify(response, {'recipes': steps})

    if request.method == 'POST':
        yield from request.read_form_data()
        data = request.form
        for key in data.keys():
            data[key] = data[key][0]
        if data.get('recipe_name'):
            Step.create(data)
            steps = {'steps': list(Step.filter(recipe_name=data.get('recipe_name')))}
            yield from picoweb.jsonify(response, {'steps': steps})



@app.route(re.compile('^/api/steps/(.+)'), methods=['GET'])
def step(request, response):
    pkey = picoweb.utils.unquote_plus(request.url_match.group(1))
    steps = list(Step.filter(recipe_name=pkey))
    print(steps)
    yield from picoweb.jsonify(response, {'steps': steps})

