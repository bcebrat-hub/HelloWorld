from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return "Hello World from Ben Cebrat! I am adding my first code change."

@app.route('/hello')
def hello():
    return "Hello World from Ben Cebrat! This is my first HTML page."
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("About.html")

if __name__ == "__main__":
    app.run(debug=True)