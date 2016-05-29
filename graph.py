import plotly.plotly as py
import plotly.tools as tls
import plotly.graph_objs as go

username = 'chuckry'
api_key  = '799l3tg6mq'
tls.set_credentials_file(username=username, api_key=api_key)

def createGraph(data):

	traces = []
	partners = []
	phrase = ""

	for partner in data['Films']:
		x      = []
		y      = []
		titles = []
		val    = 1
		partners.append(partner)

		for films in data['Films'][partner]:
			x.append(val)
			titles.append(films[0])
			y.append(films[2])
			val += 1

		traces.append(go.Scatter(
			x = x,
			y = y,
			mode = "lines+markers",
			name = partner,
			text = titles
		))

	if len(partners) > 1:
		for partner in partners:
			phrase += partner + ", "
		phrase = phrase[:-2]
	else:
		phrase = str(partners[0])

	layout = go.Layout(
		title=data['Person'] + " and " + phrase,
		xaxis = {
			'title': 'Date of Release'
		},
		yaxis = {
			'title': 'Tomatoscore'
		}
	)

	figure = go.Figure(data=traces, layout=layout)
	plot_url = py.plot(figure, filename='Film Pairs', auto_open=False)

	return tls.get_embed(plot_url)