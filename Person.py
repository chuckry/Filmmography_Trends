import operator

class Person:
	def __init__(self, name, _type, ID):
		self.name       = name
		self.type       = _type
		self.ID         = ID
		self.movies     = []
		self.associates = {}

	def update_movies(self, movies):
		self.movies.append(movies)

	def is_actor(self):
		return self.type == "with_cast"
	
	def is_director(self):
		return self.type == "with_crew"

	def update_hash(self, key):
		if key not in self.associates:
			self.associates[key] = 1
		else:
			self.associates[key] += 1

	def combine_pages(self):
		movies = []
		for page in self.movies:
			for movie in page['results']:
				movies.append(movie)
		self.movies = movies

	def sort_hash(self):
		return sorted(self.associates.items(), key=operator.itemgetter(1))