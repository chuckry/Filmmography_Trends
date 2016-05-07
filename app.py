from flask import Flask, render_template, request, json
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
		return json.dumps(duos.run(_name, _type))
	else:
		return json.dumps({'html':'<span>Complete required fields!</span>'})

if __name__ == "__main__":
	app.debug = True
	app.run()