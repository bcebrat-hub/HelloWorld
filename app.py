from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'terpsys-secret-key'

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

# ---------- Models ----------
class Student(db.Model):
    __tablename__ = 'students'
    id        = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(50),  nullable=False)
    lastName  = db.Column(db.String(50),  nullable=False)
    email     = db.Column(db.String(100), nullable=False)
    major     = db.Column(db.String(50),  nullable=False)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50),  nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    role     = db.Column(db.String(20),  nullable=False)  # STUDENT, MANAGER, ADMIN

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ---------- Auth Routes ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('home'))
        return render_template('login.html', error='Invalid username or password.')
    return render_template('login.html', error=None)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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

# ---------- Training Route (MANAGER or ADMIN only) ----------
@app.route('/training')
@login_required
def training():
    if current_user.role not in ['MANAGER', 'ADMIN']:
        return redirect(url_for('home'))
    return render_template('training.html')

# ---------- CRUD Routes ----------
@app.route('/student/view')
@login_required
def view_all_students():
    students = Student.query.all()
    return render_template('viewAllStudents.html', students=students)

@app.route('/student/view/<int:student_id>')
@login_required
def view_student(student_id):
    if student_id == 0:
        student = Student.query.filter_by(email=current_user.username + '@umd.edu').first_or_404()
    else:
        student = Student.query.get_or_404(student_id)
    return render_template('viewStudent.html', student=student)

@app.route('/students/create', methods=['GET', 'POST'])
@login_required
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
@login_required
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
@login_required
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('view_all_students'))

if __name__ == "__main__":
    app.run()
