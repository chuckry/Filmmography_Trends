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
	person.get_person_ID(_name, tmdb, tmdb_key)

	# Get hash of person's coworkers and their collaborative work
	person.get_movie_list(tmdb, tmdb_key, person.get_movie_info(tmdb, tmdb_key))
	person.sort_hash()

	# Get ratings for each movie
	for associate in person.associates:
		for film in person.associates[associate]:
			film.find_ratings(omdb)

		person.associates[associate] = [film for film in person.associates[associate]
			if film.tomatoes != "N/A"]

	# Find the average rating per associate
	best_avg    = 0
	best_person = []
	for associate in person.associates:
		avg_rating   = 0
		metascores   = []
		tomatoscores = []

		for film in person.associates[associate]:
			try:
				metascores.append(int(film.metascore))
			except:
				print "Unavailable Metascore"

			tomatoscores.append(int(film.tomatoes))
		
		ratings       = np.array(tomatoscores)
		median_rating = np.median(ratings)
		mean_rating   = np.mean(ratings)
		avg_rating    = mean_rating

		# If current avg rating is better than current best, update best person/avg
		if avg_rating >= best_avg:
			if avg_rating != best_avg:
				best_person = []
				best_avg    = avg_rating

			best_person.append(associate)

	# Pack finished values into JSON-serializable format
	films = {}
	for collab in best_person:
		if collab not in films:
			films[collab] = []

		for movie in person.associates[collab]:
			films[collab].append([movie.title, movie.metascore, movie.tomatoes])

	return json.dumps({
		'Person': person.name,
		'Best Collab': best_person,
		'Avg Rating': best_avg,
		'Films': films
	})







