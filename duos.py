from Person import *
from Movie import *
import sys, pprint
import numpy as np

# App calls this function to drive program
def run(_name, _type):
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
		film = Movie(movie['title'])
		film.find_ratings(omdb)
		films.append([film.title, film.tomatoes, film.metascore, film.date])
	
	films = [x for x in films if x[3] != 0]
	return json.dumps({
		'Person': person.name,
		'Type': 'Director' if _type == 'd' else 'Actor',
		'Films': films,
		'Error': 0
	})



