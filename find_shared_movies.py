from urllib2 import Request, urlopen
import sys, json, requests, pprint

# API key, content url constants
api_key = "e6e136a71855baad76ee2360bac5595f"
url     = "http://api.themoviedb.org/3/"

# Two inputs
person      = sys.argv[1]
person_type = sys.argv[2]

# Only two options for selection
if person_type != 'd' and person_type != 'a':
	print "Must enter either \'a\' for actor or \'d\' for director."
	sys.exit()

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
def get_num_pages(person_type, ID, method):
	try:
		params = {
			'api_key': api_key,
			person_type: ID
		}

		resp = requests.get(url=url + method, params=params)
		data = json.loads(resp.content)
	except:
		"Couldn't get number of pages."
	return data['total_pages']

'''
	# Requires: Movie data in the form of a list of lists of dictionaries 
				(each element being from a different page)
	# Modifies: Nothing
	# Effects:	"Flattens" the list of lists of dicts to a list of dicts
'''
def combine_pages(movie_data):
	movies = []
	for page in movie_data:
		for movie in page['results']:
			movies.append(movie)
	return movies

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
	# Effects: 	Returns a list of results for the given ID
'''
# Takes a person's ID and their role in movies, returning their movie data
def discover_person(person_type, ID):
	person_movies = []
	method = 'discover/movie'
	pages = get_num_pages(person_type, ID, method)
	for page in range(1, pages + 1):
		try:
			params = {
				'api_key': api_key,
				person_type: ID,
				'page': page
			}
			resp = requests.get(url=url + method, params=params)
			person_movies.append(json.loads(resp.content))
		except:
			print "Movie search failed."
	return combine_pages(person_movies)

'''
	# Requires: A valid person type (actor/director) and his/her ID
	# Modifies: Nothing
	# Effects:	Returns a list of given person's movies' [titles, IDs]
'''
def get_movie_info(person_type, ID):
	try:
		if person_type == 'a':
			person_type = 'with_cast'
		elif person_type == 'd':
			person_type = 'with_crew'

		data       = discover_person(person_type, ID)
		movie_list = []

		# TODO: Write function to only append titles that have
		# already been released
		for result in data:
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
def get_movie_count(data):
	associate_count = {}
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
			if person_type == 'a':
				for member in details['crew']:
					if member['job'] == "Director":
						if member['name'] == person:
							continue
						if member['name'] not in associate_count:
							associate_count[member['name']] = 1
						else:
							associate_count[member['name']] += 1
			elif person_type == 'd':
				for actor in details['cast']:
					if actor['name'] == person:
						continue
					if actor['name'] not in associate_count:
						associate_count[actor['name']] = 1
					else:
						associate_count[actor['name']] += 1

		except:
			"Couldn't find director."
	return associate_count

# Contains hash of person's coworkers and the number of collaborations
pprint.pprint(get_movie_count(get_movie_info(person_type, get_person_ID(person))))

# TODO: Create Person and Movie objects to more cleanly organize code
#		and speed up program to avoid sending requests to TMDB server