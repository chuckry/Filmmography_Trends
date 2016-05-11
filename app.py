from flask import Flask, render_template, request, json
from Person import *
from Movie import *
import duos
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

	# Validate information
	if _name and _type:
		results = duos.run(_name, _type)
		if json.loads(results)['Error'] == 1:
			return "Couldn't find " + json.loads(results)['Person'] + "!"
		else:
			return results
	else:
		return "Complete required fields!"

if __name__ == "__main__":
	app.debug = True
	app.run()