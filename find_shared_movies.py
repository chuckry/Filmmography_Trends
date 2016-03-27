from urllib2 import Request, urlopen
import sys, json, requests, pprint

# API key, content url constants
api_key = "e6e136a71855baad76ee2360bac5595f"
url     = "http://api.themoviedb.org/3/"

# Algorithm #
# 1) User enters director name and actor name
# 2) Pass that information into /search/person and grab their IDs
# 3) Use the IDs to collect movies they've worked on
# 4) Find all mutual movies and save them to a list

# Goal: User enters actor and director names and is given an overall
# "score" of their work together with a list of their movies

actor    = sys.argv[1]
director = sys.argv[2]

# Takes in a string and passes it as a query, returning a person's ID
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

def get_num_pages(person_type, ID, method):
	try:
		params = {
			'api_key': api_key,
			person_type: ID
		}

		resp = requests.get(url=url + method, params=params)
		data = json.loads(resp.content)
		return data['total_pages']
	except:
		"Couldn't get number of pages."

# Takes a person's ID and their role in movies, returning their movie data
def discover_person(person_type, ID):
	data = []
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
			data.append(json.loads(resp.content))
		except:
			print "Movie search failed."
	return data

actor_titles    = []
director_titles = []

actor_info    = discover_person('with_cast', get_person_ID(actor))
director_info = discover_person('with_crew', get_person_ID(director))

for page in actor_info:
	for result in page['results']:
		actor_titles.append(result['title'])

for page in director_info:
	for result in page['results']:
		director_titles.append(result['title'])

collective_work = list(set(actor_titles) & set(director_titles))
pprint.pprint(collective_work)