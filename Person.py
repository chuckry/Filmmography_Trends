from Movie import *
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

	def is_actor(self):
		return self.type == "with_cast"
	
	def is_director(self):
		return self.type == "with_crew"

	def update_hash(self, key, movie):
		if key not in self.associates:
			self.associates[key] = []

		m = Movie(movie)
		self.associates[key].append(m)

	def combine_pages(self):
		movies = []
		for page in self.movies:
			for movie in page['results']:
				movies.append(movie)
		self.movies = movies

	def sort_hash(self):
		self.associates = { key: value for key, value in self.associates.items() if len(value) >= THRESHOLD }
		return self.associates

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

	'''
		# Requires: A valid person type (actor/director) and his/her ID
		# Modifies: Nothing
		# Effects:	Returns a list of given person's movies' [titles, IDs]
	'''
	def get_movie_info(self, url, api_key):
		self.discover_person(url, api_key)
		movie_list = []

		# TODO: Write function to only append titles that have
		# already been released by current date
		for result in self.movies:
			movie_list.append( [result['title'], result['id']] )
		return movie_list

	'''
	# Requires: Movie info data for a person in the form [title, ID]
	# Modifies: Nothing
	# Effects: 	Returns dictionary of movie collaborators to a count of their
				appearances in all the person's movies
	'''
	def get_movie_list(self, url, api_key, movie_info):
		for movie in movie_info:
			try:
				params = {
					'api_key': api_key
				}
				resp = requests.get(url=url + "movie/" + str(movie[1]) + "/credits",
					params=params)
				details = json.loads(resp.content)

				# Iterate through each member of the crew and increment
				# this director's count
				if self.is_actor():
					for member in details['crew']:
						if member['job'] == "Director":
							if member['name'] == self.name:
								continue
							else:
								self.update_hash(member['name'], movie[0])
				elif self.is_director():
					for actor in details['cast']:
						if actor['name'] == self.name:
							continue
						else:
							self.update_hash(actor['name'], movie[0])
			except:
				print details['status_code'],": ",details['status_message']
				return
