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

	'''
		# Requires: Movie data in the form of a list of lists of dictionaries 
					(each element being from a different page)
		# Modifies: Nothing
		# Effects:	"Flattens" the list of lists of dicts to a list of dicts
	'''
	def combine_pages(self):
		movies = []
		for page in self.movies:
			for movie in page['results']:
				movies.append(movie)
		self.movies = movies