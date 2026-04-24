from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.secret_key = "supersecretkey"

# ---------------- DATABASE CONFIG ----------------

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Create tables safely
with app.app_context():
    db.create_all()

# ---------------- MODELS ----------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default="user")  # user / admin


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(db.String(20), default="Low")
    status = db.Column(db.String(50), default="Open")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- HELPER ----------------

def is_admin():
    return session.get("role") == "admin"

# ---------------- ROUTES ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        existing_user = User.query.filter_by(
            username=request.form["username"]
        ).first()

        if existing_user:
            return render_template("register.html", error="Username already exists")

        user = User(
            username=request.form["username"],
            password=generate_password_hash(request.form["password"]),
            role="user"
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template("register.html")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None

    if request.method == "POST":
        user = User.query.filter_by(
            username=request.form["username"]
        ).first()

        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            session["username"] = user.username
            session["role"] = user.role
            return redirect("/dashboard")

        error = "Invalid username or password"

    return render_template("login.html", error=error)


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    return render_template("dashboard.html", username=session["username"])


# ---------------- CREATE TICKET ----------------

@app.route("/create_ticket", methods=["GET", "POST"])
def create_ticket():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        ticket = Ticket(
            user_id=session["user_id"],
            title=request.form["title"],
            description=request.form["description"],
            priority=request.form.get("priority", "Low")
        )

        db.session.add(ticket)
        db.session.commit()

        return redirect("/my_tickets")

    return render_template("create_ticket.html")


# ---------------- USER TICKETS ----------------

@app.route("/my_tickets")
def my_tickets():
    if "user_id" not in session:
        return redirect("/login")

    tickets = Ticket.query.filter_by(user_id=session["user_id"]).all()
    return render_template("my_tickets.html", tickets=tickets)


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- ADMIN PANEL ----------------

@app.route("/admin")
def admin():
    if not is_admin():
        return redirect("/login")

    tickets = Ticket.query.all()
    return render_template("admin.html", tickets=tickets)


# ---------------- UPDATE STATUS ----------------

@app.route("/update_status/<int:id>/<status>")
def update_status(id, status):
    if not is_admin():
        return redirect("/login")

    ticket = db.session.get(Ticket, id)

    if ticket:
        ticket.status = status
        db.session.commit()

    return redirect("/admin")


# ---------------- ADMIN STATS ----------------

@app.route("/admin_stats")
def admin_stats():
    if not is_admin():
        return redirect("/login")

    total = Ticket.query.count()
    open_t = Ticket.query.filter_by(status="Open").count()
    closed = Ticket.query.filter_by(status="Closed").count()

    return render_template(
        "admin_stats.html",
        total=total,
        open_t=open_t,
        closed=closed
    )


# ---------------- USER MANAGEMENT ----------------

@app.route("/admin_users")
def admin_users():
    if not is_admin():
        return redirect("/login")

    users = User.query.all()
    return render_template("admin_users.html", users=users)


# ---------------- PROMOTE USER TO ADMIN ----------------

@app.route("/make_admin/<int:user_id>")
def make_admin(user_id):
    if not is_admin():
        return redirect("/login")

    user = db.session.get(User, user_id)

    if user:
        user.role = "admin"
        db.session.commit()

    return redirect("/admin_users")


# ---------------- SEARCH ----------------

@app.route("/search")
def search():
    query = request.args.get("q", "")

    tickets = Ticket.query.filter(
        Ticket.title.contains(query)
    ).all()

    return render_template("my_tickets.html", tickets=tickets)


# ---------------- RUN APP ----------------

if __name__ == "__main__":
    app.run(debug=True)