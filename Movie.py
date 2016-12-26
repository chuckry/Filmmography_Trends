import sys, requests, json

# Converts given string for a month into the corresponding numeral:
MONTH_HASH = {
	"Jan": '1',
	"Feb": '2',
	"Mar": '3',
	"Apr": '4',
	"May": '5',
	"Jun": '6',
	"Jul": '7',
	"Aug": '8',
	"Sep": '9',
	"Oct": '10',
	"Nov": '11',
	"Dec": '12'
}

class Movie:
	def __init__(self, title):
		self.title     = title
		self.ID        = 0
		self.metascore = 0
		self.tomatoes  = 0
		self.imdb      = 0
		self.date      = 0

	# Send request to get multiple ratings for this movie
	def find_ratings(self, url):
		try:
			params = {
				't': self.title,
				'tomatoes': 'true'
			}
			resp = requests.get(url=url, params=params)
			data = json.loads(resp.content)
			
			self.ID        = data['imdbID']
			self.metascore = data['Metascore']
			self.tomatoes  = data['tomatoMeter']
			self.imdb      = data['imdbRating']

			date_info = data['Released'].split(' ')
			self.date = MONTH_HASH[date_info[1]] + '/' + str(date_info[0]) + '/' + str(date_info[2])

		except:
			print "Issue with data retrieval"
			return

	# Debugging purposes
	def print_ratings(self):
		print "-----", self.title, "-----"
		print "IMDB:\t\t", self.imdb
		print "Metacritic:\t", self.metascore
		print "Rotten Tomatoes\t", self.tomatoes
		print ""






