from flask import Flask, render_template

aplication = Flask(__name__)

@aplication.route('/')
def home():
	return render_template("home.html")

@aplication.route('/about/')
def about():
	return render_template("about.html")

if __name__ == "__main__":
	aplication.run(debug = True)