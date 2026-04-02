from app import app, db, Student, User
from werkzeug.security import generate_password_hash

with app.app_context():
    db.create_all()

    if not Student.query.filter_by(email='bcebrat@umd.edu').first():
        me = Student(
            firstName='Ben',
            lastName='Cebrat',
            email='bcebrat@umd.edu',
            major='Finance and Information Systems'
        )
        db.session.add(me)

    if not User.query.filter_by(username='bcebrat').first():
        me_user = User(
            username='bcebrat',
            password=generate_password_hash('bcebrat'),
            role='STUDENT'
        )
        db.session.add(me_user)

    db.session.commit()
    print("Database created and seeded successfully.")