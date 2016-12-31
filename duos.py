from Person import *
import sys, pprint
import numpy as np

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

def genresMatch(condition, genres, film):
	if condition == "and":
		return set(genres) < set(film[4])
	if condition == "or":
		return bool(set.intersection(set(genres), set(film[4])))
	return None

def filterByCriteria(films, excl, genres, runtime):
	filteredFilms = []
	for film in films:
		if film and film[3] != 0:
			if genresMatch(excl, genres, film):
				filteredFilms.append(film)
	filteredFilms = [x for x in filteredFilms if x[5] <= runtime]
	return filteredFilms

def find_ratings(title, url):
	try:
		params = {
			't': title,
			'tomatoes': 'true'
		}
		resp = requests.get(url=url, params=params)
		data = json.loads(resp.content)

		metascore = data['Metascore']
		tomatoes  = data['tomatoMeter']
		genres    = data['Genre'].split(',')
		runtime   = int(data['Runtime'].split(' ')[0])
		date_info = data['Released'].split(' ')
		date = MONTH_HASH[date_info[1]] + '/' + str(date_info[0]) + '/' + str(date_info[2])
		return [title, tomatoes, metascore, date, genres, runtime]

	except:
		print "Issue with data retrieval"
		return


# App calls this function to drive program
def run(_name, _type, _excl, _genres, runtime):
	# API key, content url constants
	tmdb_key = "e6e136a71855baad76ee2360bac5595f"
	tmdb     = "http://api.themoviedb.org/3/"
	omdb     = 'http://www.omdbapi.com/'

	# Only two options for selection
	if _type != 'd' and _type != 'a':
		print "Must enter either \'a\' for actor or \'d\' for director."
		sys.exit()

	# Two inputs
	t = ''
	if _type == 'a':
		t = 'with_cast' 
	if _type == 'd':
		t = 'with_crew' 

	person = Person(_name, t)
	if person.get_person_ID(_name, tmdb, tmdb_key) == 0:
		return json.dumps({
			'Error': 1,
			'Person': person.name
		})

	# Get hash of person's coworkers and their collaborative work
	person.discover_person(tmdb, tmdb_key)
	films = []
	for movie in person.movies:
		films.append(find_ratings(movie['title'], omdb))
	
	films = filterByCriteria(films, _excl, _genres, runtime)

	return json.dumps({
		'Person': person.name,
		'Type': 'Director' if _type == 'd' else 'Actor',
		'Films': films,
		'Error': 0
	})