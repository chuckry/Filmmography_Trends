import operator, pprint, sys, requests, json

THRESHOLD = 3

class Person:
	def __init__(self, name, _type):
		self.name           = name
		self.type           = _type
		self.ID             = 0
		self.movies         = []
		self.associates     = {}

	def update_movies(self, movies):
		self.movies.append(movies)

	def combine_pages(self):
		movies = []
		for page in self.movies:
			for movie in page['results']:
				movies.append(movie)
		self.movies = movies

	'''
	# Requires: A query string
	# Modifies: Nothing
	# Effects:	Finds the TMDB ID corresponding to the given query
	'''
	def get_person_ID(self, query, url, api_key):
		try:
			params = {
				'api_key': api_key,
				'query': query
			}
			resp = requests.get(url=url + 'search/person', params=params)
			data = json.loads(resp.content)
			self.ID = data['results'][0]['id']
			return 1
		except:
			return 0
			sys.exit()

	'''
	# Requires: A valid person type, person ID, and method
	# Modifies: Nothing
	# Effects:	Gets the total number of pages of results for a given
				input and method
	'''
	def get_num_pages(self, url, api_key, method):
		params = {
			'api_key': api_key,
			self.type: self.ID
		}

		resp = requests.get(url=url + method, params=params)
		data = json.loads(resp.content)
		return data['total_pages']

	'''
		# Requires: A valid person type and his/her ID
		# Modifies: Nothing
		# Effects: 	Returns a list of movies for the given ID
	'''
	def discover_person(self, url, api_key):
		self_movies = []
		method        = 'discover/movie'
		pages         = self.get_num_pages(url, api_key, method)

		for page in range(1, pages + 1):
			try:
				params = {
					'api_key': api_key,
					self.type: self.ID,
					'page': page
				}
				resp = requests.get(url=url + method, params=params)
				self.update_movies(json.loads(resp.content))
			except:
				print "Movie search failed."
				sys.exit()
		self.combine_pages()