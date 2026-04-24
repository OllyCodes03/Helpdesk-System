from app import app, db, User
from werkzeug.security import generate_password_hash

admin_username = input("Enter admin username: ")
admin_password = input("Enter admin password: ")

with app.app_context():

    existing = User.query.filter_by(username=admin_username).first()

    if existing:
        existing.role = "admin"
        existing.password = generate_password_hash(admin_password)

        db.session.commit()

        print("Admin updated")
    else:
        admin = User(
            username=admin_username,
            password=generate_password_hash(admin_password),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created")

