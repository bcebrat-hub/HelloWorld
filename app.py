from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("About.html")
@app.route('/about-css')
def about_css():
    return render_template('about-css.html') #fixed

@app.route('/favorite-course')
def favorite_course():
    subject = request.args.get('subject', '')
    course_number = request.args.get('course_number', '')
    return render_template('favorite-course.html', subject=subject, course_number=course_number)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        first_name = request.form.get('first_name', '')
        last_name  = request.form.get('last_name', '')
        email      = request.form.get('email', '')
        major      = request.form.get('major', '')
        return render_template('contact.html', submitted=True,
                               first_name=first_name, last_name=last_name,
                               email=email, major=major)
    return render_template('contact.html', submitted=False)
@app.route("/hello")
def hello():
    return "Hello World from Ben Cebrat! This is my first HTML page."

@app.route("/hi")
def hello_world():
    return "Hello World from Ben Cebrat! I am adding my first code change."

if __name__ == "__main__":
    app.run()
