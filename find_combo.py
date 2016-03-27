from urllib2 import Request, urlopen
from find_shared_movies import *
import sys, json, requests, pprint

# Takes input as either a director or an actor, given by a flag
# 1) Searches that actor/director through TMDB
# 2) Finds their most common coworker using dictionary

api_key = "e6e136a71855baad76ee2360bac5595f"
url     = "http://api.themoviedb.org/3/"

person      = sys.argv[1]
person_type = sys.argv[2]

if person_type != 'd' and person_type != 'a':
	print "Must enter either \'a\' for actor or \'d\' for director."
	sys.exit()

# Input is an array of movie titles (strings)
# Output is a dictionary of [director, movie count for given actor]
# TODO: Modify to accept return actors as well
def get_movie_count(person_type, data):
	director_count = {}
	for movie in data:
		try:
			params = {
				'api_key': api_key
			}
			resp = requests.get(url=url + "movie/" + str(movie[1]) + "/credits",
				params=params)
			details = json.loads(resp.content)


			# Iterate through each member of the crew and increment
			# this director's count
			# print movie[0]
			if person_type == 'a':
				for member in details['crew']:
					if member['job'] == "Director":
						if member['name'] == person:
							continue
						if member['name'] not in director_count:
							director_count[member['name']] = 1
						else:
							director_count[member['name']] += 1
			elif person_type == 'd':
				for actor in details['cast']:
					if actor['name'] == person:
						continue
					if actor['name'] not in director_count:
						director_count[actor['name']] = 1
					else:
						director_count[actor['name']] += 1

		except:
			"Couldn't find director."
	return director_count

# 1) Given a person's ID, gather list of movies they've worked on
# 2) Given a list of movies, find the starring actors/main directors
# 3) Hash each of these connections and count
def find_pairs(person_type, ID):
	try:
		if person_type == 'a':
			person_type = 'with_crew'
		elif person_type == 'd':
			person_type = 'with_cast'

		data = discover_person(person_type, ID)
		movie_list = []

		for page in data:
			for result in page['results']:
				# TODO: Write function to only append titles that have
				# already been released
				movie_list.append( [result['title'], result['id']] )
	except:
		print "Pairing failed."
	return movie_list
pprint.pprint(get_movie_count(person_type, find_pairs(person_type, get_person_ID(person))))


