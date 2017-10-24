#'/api/'
api = {
	'recipes': 'host:port/api/recipes',
	'multicooker': 'host:port/api/multicooker'
}

#'/api/recepts'
recipes = {'recipes':
	[
		{
			'name': 'Pasta',
			'url': 'host:port/api/recipes/1',
			'description': 'Beatieful pasta',
		},
		{
			'name': 'Tea',
			'url': 'host:port/api/recipes/2',
			'description': 'Hoat tea',
		}
	]
}

#'/api/recepts/1'
recipe = {
	'name': 'Pasta',
	'url': 'host:port/api/recipes/1',
	'start': 'host:port/api/multicooker?start=1',
	'stop': 'host:port/api/multicooker?stop=',
	'description': 'Delicious pasta',
	'steps':
	[
		{
			'id': '1',
			'time': '10',
			'temperature': '100',
			'wait': '1',
			'description': 'Heat water'
		},
		{
			'id': '2',
			'time': '5',
			'temperature': '120',
			'wait': '0',
			'description': 'Put pasta'
		},
	]
}

#'/api/multicooker'
multicooker = {
	'start': 'host:port/api/multicooker?start=<recept_id>',
	'stop': 'host:port/api/multicooker?stop=', 
	'recipe': 
	{
		'name': 'Pasta',
		'url': 'host:port/api/recipes/1',
		'step': '2',
		'time_left': '7',
		'temperature': '98'
	}
}
