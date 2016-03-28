from urllib2 import Request, urlopen
from Person import *
import sys, json, requests, pprint

# API key, content url constants
api_key = "e6e136a71855baad76ee2360bac5595f"
url     = "http://api.themoviedb.org/3/"



'''
	# Requires: A query string
	# Modifies: Nothing
	# Effects:	Finds the TMDB ID corresponding to the given query
'''
def get_person_ID(query):
	try:
		params = {
			'api_key': api_key,
			'query': query
		}
		resp = requests.get(url=url + 'search/person', params=params)
		data = json.loads(resp.content)
		return data['results'][0]['id']
	except:
		print "Person search failed."



'''
	# Requires: A valid person type, person ID, and method
	# Modifies: Nothing
	# Effects:	Gets the total number of pages of results for a given
				input and method
'''
def get_num_pages(person, method):
	try:
		params = {
			'api_key': api_key,
			person.type: person.ID
		}

		resp = requests.get(url=url + method, params=params)
		data = json.loads(resp.content)
	except:
		"Couldn't get number of pages."
	return data['total_pages']



'''
	# Requires: A list of movies
	# Modifies: Nothing
	# Effects:	Extracts the titles of each movie and prints it out. Used
				mainly for debugging to display title data clearly
'''
def extract_titles(movies):
	titles = []
	for result in movies:
		titles.append(result['title'])
	return titles



'''
	# Requires: A valid person type and his/her ID
	# Modifies: Nothing
	# Effects: 	Returns a list of movies for the given ID
'''
def discover_person(person):
	person_movies = []
	method        = 'discover/movie'
	pages         = get_num_pages(person, method)

	for page in range(1, pages + 1):
		try:
			params = {
				'api_key': api_key,
				person.type: person.ID,
				'page': page
			}
			resp = requests.get(url=url + method, params=params)
			person.update_movies(json.loads(resp.content))
		except:
			print "Movie search failed."
	person.combine_pages()



'''
	# Requires: A valid person type (actor/director) and his/her ID
	# Modifies: Nothing
	# Effects:	Returns a list of given person's movies' [titles, IDs]
'''
def get_movie_info(person):
	try:
		discover_person(person)
		movie_list = []

		# TODO: Write function to only append titles that have
		# already been released by current date
		for result in person.movies:
			movie_list.append( [result['title'], result['id']] )
	except:
		print "Pairing failed."
	return movie_list



'''
	# Requires: Movie info data for a person in the form [title, ID]
	# Modifies: Nothing
	# Effects: 	Returns dictionary of movie collaborators to a count of their
				appearances in all the person's movies
'''
def get_movie_count(person, movie_info):
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
			if person.is_actor():
				for member in details['crew']:
					if member['job'] == "Director":
						if member['name'] == person.name:
							continue
						else:
							person.update_hash(member['name'])
			elif person.is_director():
				for actor in details['cast']:
					if actor['name'] == person.name:
						continue
					else:
						person.update_hash(actor['name'])

		except:
			"Couldn't find director."

# Only two options for selection
if sys.argv[2] != 'd' and sys.argv[2] != 'a':
	print "Must enter either \'a\' for actor or \'d\' for director."
	sys.exit()

t = ''
# Two inputs
if sys.argv[2] == 'a':
	t = 'with_cast' 
if sys.argv[2] == 'd':
	t = 'with_crew' 
person = Person(sys.argv[1], t, get_person_ID(sys.argv[1]))


# Contains hash of person's coworkers and the number of collaborations
get_movie_count(person, get_movie_info(person))
pprint.pprint(person.associates)

# TODO:
# - Create Movie object
# - Write small test cases to run









