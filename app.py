from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ---------- Student Model ----------
class Student(db.Model):
    __tablename__ = 'students'
    id        = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50),  nullable=False)
    lastName  = db.Column(db.String(50),  nullable=False)
    email     = db.Column(db.String(100), nullable=False)
    major     = db.Column(db.String(50),  nullable=False)

# ---------- Existing Routes ----------
@app.route("/")
def home():
    return render_template("About.html")

@app.route('/about-css')
def about_css():
    return render_template('about-css.html')

@app.route('/favorite-course')
def favorite_course():
    subject       = request.args.get('subject', '')
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

# ---------- CRUD Routes ----------
@app.route('/student/view')
def view_all_students():
    students = Student.query.all()
    return render_template('viewAllStudents.html', students=students)

@app.route('/students/<int:student_id>')
def view_student(student_id):
    student = Student.query.get_or_404(student_id)
    return render_template('viewStudent.html', student=student)

@app.route('/students/create', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        new_student = Student(
            firstName = request.form.get('firstName'),
            lastName  = request.form.get('lastName'),
            email     = request.form.get('email'),
            major     = request.form.get('major')
        )
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('view_all_students'))
    return render_template('addStudent.html')

@app.route('/student/update/<int:student_id>', methods=['GET', 'POST'])
def update_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.firstName = request.form.get('firstName')
        student.lastName  = request.form.get('lastName')
        student.email     = request.form.get('email')
        student.major     = request.form.get('major')
        db.session.commit()
        return redirect(url_for('view_all_students'))
    return render_template('updateStudent.html', student=student)

@app.route('/student/delete/<int:student_id>', methods=['POST'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('view_all_students'))

if __name__ == "__main__":
    app.run()
