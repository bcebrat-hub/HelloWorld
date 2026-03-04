from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("About.html")
@app.route('/about-css')
def about_css():
    return render_template('about-css.html')

@app.route("/hello")
def hello():
    return "Hello World from Ben Cebrat! This is my first HTML page."

@app.route("/hi")
def hello_world():
    return "Hello World from Ben Cebrat! I am adding my first code change."

if __name__ == "__main__":
    app.run()
