#from .app import app
#from .models import Recipe, Step
from app import app
from models import Recipe, Step

import ure as re
import picoweb
#from . import ijson
import ijson

host = "127.0.0.1"
port = 8081
host_port = 'http://' + host + ':' + str(port) 


@app.route('/')
def index(request, response):
    yield from picoweb.start_response(response)
    Recipes = Recipe.scan()
    steps = Recipe.scan()
    #print(list(steps))
    yield from app.render_template(response, 'index.html', (Recipes,steps,))


@app.route('/api', methods=['GET'])
def api(request, response):
    api_url = {
        'recipes': host_port + '/api/recipes',
        'multicooker': host_port + '/api/multicooker'
    }
    yield from picoweb.jsonify(response, api_url)


@app.route('/api/recipes', methods=['GET', 'POST'])
def recipes(request, response):
    print(request.method)
    if request.method == 'POST':
        print(request.headers)
        yield from request.read_form_data()
        print(request.form)
        if request.form.get('content'):
            print(2)
        print(3)
        yield from picoweb.jsonify(response, {'success': 0})
        return

    recipes = Recipe.all()
    r = []
    for recipe in recipes:
        recipe['url'] = host_port + '/api/recipes/' + recipe['id']
        recipe.pop('id')
        r.append(recipe)
    yield from picoweb.jsonify(response, {'recipes': r})


@app.route(re.compile('^/api/recipes/(.+)'), methods=['GET'])
def recipe(request, response):
    pkey = picoweb.utils.unquote_plus(request.url_match.group(1))
    steps = Step.filter_on_recipe(pkey)
    s = []
    for step in steps:
        s.append(step)
    recipe = Recipe.get_id(pkey)
    if recipe:
        recipe['steps'] = s
        recipe['url'] = host_port + '/api/recipes/' + recipe['id']
        recipe['start'] = host_port + '/api/multicooker?start=' + recipe['id']
        recipe['stop'] = host_port + '/api/multicooker?stop='
        recipe.pop('id')
    yield from picoweb.jsonify(response, {'recipes': recipe})



'''
@app.route('/', methods=['GET', 'POST'])
def homepage(request, response):
    if request.method == 'POST':
        print(request.headers)
        yield from request.read_form_data()
        if request.form.get('content'):
            note_id = Note.create(content=request.form['content'][0])
            note = list(Note.get_id(note_id))[0]
            print("note after create:", note)
            tmpl = app._load_template('note.html')
            yield from picoweb.start_response(response, "application/json")
            yield from response.awriteiter(ijson.idumps({'note': tmpl(note), 'success': 1}))
            return

        yield from picoweb.jsonify(response, {'success': 0})
        return

    yield from picoweb.start_response(response)
#    notes = Note.public().paginate(get_page(), 50)
    notes = Note.public()
    yield from app.render_template(response, 'homepage.html', (notes,))

@app.route(re.compile('^/archive/(.+)'), methods=['POST'])
def archive_note(request, response):
    pkey = picoweb.utils.unquote_plus(request.url_match.group(1))
    print("archive_note", pkey)
    Note.update({"timestamp": pkey}, archived=1)
    yield from picoweb.jsonify(response, {'success': True})
'''