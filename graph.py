import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go
import pprint

username = 'chuckry'
api_key  = '799l3tg6mq'
tls.set_credentials_file(username=username, api_key=api_key)

MONTH_LENGTHS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

# Returns a boolean denoting whether the given year is a leap year or not
def isLeapYear(year):
	return year % 4 == 0 and not (year % 100 == 0 and year % 400 != 0)

# Converts a slash-delimited date into a float
def dateScore(date):
	if date.find('/') == -1:
		"Incorrect date format."
		exit(1)

	month, day, year = map(float, date.split('/'))
	monthBuffer = sum(MONTH_LENGTHS[x] for x in xrange(0, int(month) - 1))
	monthBuffer += 1 if isLeapYear(year) and month == 2 else 0
	return year + (monthBuffer + day) / 365.0

# Creates a graph to visualize the given celebrity's film scores
def createGraph(data):
	traces = []
	releaseDates = []
	rtScores     = []
	metaScores   = []
	titles       = []

	for film in data['Films']:
		film[3] = dateScore(film[3])

	data['Films'].sort(key=lambda x: x[3])

	for film in data['Films']:
		if 'N/A' in film:
			continue
		titles.append(film[0])
		rtScores.append(film[1])
		metaScores.append(film[2])
		releaseDates.append(film[3])

	traces.append(go.Scatter(
		x = releaseDates,
		y = rtScores,
		mode = "lines+markers",
		name = 'Tomatoscore',
		text = titles
	))

	traces.append(go.Scatter(
		x = releaseDates,
		y = metaScores,
		mode = "lines+markers",
		name = 'Metascore',
		text = titles
	))

	layout = go.Layout(
		title = data['Person'] + ": " + data['Type'],
		xaxis = {
			'title': 'Date of Release'
		},
		yaxis = {
			'title': 'Rating'
		}
	)

	figure = go.Figure(data=traces, layout=layout)
	plot_url = py.plot(figure, filename='Filmography', auto_open=False)
	return tls.get_embed(plot_url)