from flask import Flask, render_template, request, json
from Person import *
from Movie import *
import duos
import graph
import pprint
app = Flask(__name__)

# Sends user to homepage to enter their query
@app.route('/')
def main():
	return render_template('index.html')

# Sends user to view results
# TODO: Create results page so that users can re-enter queries
@app.route('/', methods=['POST'])
def entry():
	# Read posted values
	_name = request.form['inputName']
	_type = request.form['inputType']
	_excl = request.form['exclusivity']
	_genres = request.form.getlist('check')
	_runtime = request.form['runtime']

	# Validate information
	if _name and _type:
		results = json.loads(duos.run(_name, _type, _excl, _genres, _runtime))
		if results['Error'] == 1:
			return "Couldn't find " + json.loads(results)['Person'] + "!"
		else:
			# pprint.pprint(results)
			return graph.createGraph(results)
	else:
		return "Complete required fields!"

if __name__ == "__main__":
	app.debug = True
	app.run()