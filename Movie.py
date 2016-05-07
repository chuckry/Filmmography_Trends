import sys, requests, json

class Movie:
	def __init__(self, name):
		self.name      = name
		self.ID        = 0
		self.metascore = 0
		self.tomatoes  = 0
		self.imdb      = 0

	# Send request to get multiple ratings for this movie
	def find_ratings(self, url):
		try:
			params = {
				't': self.name,
				'tomatoes': 'true'
			}
			resp = requests.get(url=url, params=params)
			data = json.loads(resp.content)
			
			self.ID        = data['imdbID']
			self.metascore = data['Metascore']
			self.tomatoes  = data['tomatoMeter']
			self.imdb      = data['imdbRating']

		except:
			return

	# Debugging purposes
	def print_ratings(self):
		print "-----", self.name, "-----"
		print "IMDB:\t\t", self.imdb
		print "Metacritic:\t", self.metascore
		print "Rotten Tomatoes\t", self.tomatoes
		print ""