import functools
from server import app, db
from server.models import *
from flask import redirect, url_for, render_template, flash, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from . import scrape

def login_admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "type" not in session:
            flash("Login Required")
            return redirect(url_for("login"))
        elif session["type"] != "admin":
            flash("Not accessible")
        else:
            return view(**kwargs)
    return wrapped_view


def login_student_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "type" not in session:
            flash("Login Required")
            return redirect(url_for("login"))
        elif session["type"] != "student":
            flash("Not Accessible")
        else:
            return view(**kwargs)
    return wrapped_view

    
def logged_in_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "name" not in session:
            flash("Login Required")
            return redirect(url_for("login"))
        else:
            return view(**kwargs)
    return wrapped_view
    

def logged_out_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if "name" in session:
            flash("Not Accessible")
        else:
            return view(**kwargs)
    return wrapped_view


@app.route("/register/", methods = ("GET", "POST"))
@logged_out_required
def register():
    if request.method == "POST":
        if request.form["choice"] == "Student":
            return redirect(url_for("register_student"))
        else:
            return redirect(url_for("register_admin"))
    else:
        return render_template("auth/register.html")


# To-do:
# - web-scraping for cgpi, name
# - checks on the form
@app.route("/register_student/", methods = ("GET", "POST"))
@logged_out_required
def register_student():
    if request.method == "POST":
        roll_number_1 = request.form["roll_number_1"]
        roll_number_2 = request.form["roll_number_2"]
        roll_number_3 = request.form["roll_number_3"]
        name_1 = "foo"
        name_2 = "foo"
        name_3 = "foo"
        email_id_1 = str(roll_number_1) + "@nith.ac.in"
        email_id_2 = str(roll_number_2) + "@nith.ac.in"
        email_id_3 = str(roll_number_3) + "@nith.ac.in"
        phone_number_1 = request.form["phone_number_1"]
        phone_number_2 = request.form["phone_number_2"]
        phone_number_3 = request.form["phone_number_3"]
        cgpi_1 = 0.00
        cgpi_2 = 0.00
        cgpi_3 = 0.00
        year_1 = 2000 + int(roll_number_1[ : 2])
        year_2 = 2000 + int(roll_number_2[ : 2])
        year_3 = 2000 + int(roll_number_3[ : 2])
        password = generate_password_hash(request.form["password"])
        if Student.query.filter_by(roll_number = roll_number_1).first() is not None:
            print("Roll number: {} already registered.".format(roll_number_1))
            return redirect(url_for("register_student"))
        elif Student.query.filter_by(roll_number = roll_number_2).first() is not None:
            print("Roll number: {} already registered.".format(roll_number_2))
            return redirect(url_for("register_student"))
        elif Student.query.filter_by(roll_number = roll_number_3).first() is not None:
            print("Roll number: {} already registered.".format(roll_number_3))
            return redirect(url_for("register_student"))
        elif roll_number_1 == roll_number_2 or roll_number_1 == roll_number_3 or roll_number_2 == roll_number_3:
            print("Roll numbers can't be same")
            return redirect(url_for("register_student"))
        else:
            student_1 = Student(
                roll_number = roll_number_1,
                name = name_1,
                email_id = email_id_1,
                phone_number = phone_number_1,
                cgpi = cgpi_1,
                year = year_1,
                password = password
            )
            db.session.add(student_1)
            db.session.commit()
            student_2 = Student(
                roll_number = roll_number_2,
                name = name_2,
                email_id = email_id_2,
                phone_number = phone_number_2,
                cgpi = cgpi_2,
                year = year_2,
                password = password
            )
            db.session.add(student_2)
            db.session.commit()
            student_3 = Student(
                roll_number = roll_number_3,
                name = name_3,
                email_id = email_id_3,
                phone_number = phone_number_3,
                cgpi = cgpi_3,
                year = year_3,
                password = password
            )
            db.session.add(student_3)
            db.session.commit()
            team = Team(
                size = 3,
                is_lock = False
            )
            db.session.add(team)
            db.session.commit()
            member_1 = Member(
                student_id = student_1.id,
                team_id = team.id
            )
            db.session.add(member_1)
            db.session.commit()
            member_2 = Member(
                student_id = student_2.id,
                team_id = team.id
            )
            db.session.add(member_2)
            member_3 = Member(
                student_id = student_3.id,
                team_id = team.id
            )
            db.session.add(member_3)
            db.session.commit()
            print("Team registered")
            return redirect(url_for("home_page"))
    else:
        return render_template("auth/register_student.html")

        
@app.route("/register_admin/", methods = ("GET", "POST"))
@logged_out_required
def register_admin():
    if request.method == "POST":
        user_name = request.form["user_name"]
        password = generate_password_hash(request.form["password"])
        if Admin.query.filter_by(user_name = user_name).first() is not None:
            print("Admin: {} already exists.".format(user_name))
            return redirect(url_for("register_admin"))
        else:
            admin = Admin(
                user_name = user_name,
                password = password
            )
            db.session.add(admin)
            db.session.commit()
            print("Admin: {} registered.".format(user_name))
            return redirect(url_for("home_page"))
    else:
        return render_template("auth/register_admin.html")


@app.route("/login/", methods = ("GET", "POST"))
@logged_out_required
def login():
    if request.method == "POST":
        if request.form["choice"] == "Student":
            return redirect(url_for("login_student"))
        else:
            return redirect(url_for("login_admin"))
    else:
        return render_template("auth/login.html")


@app.route("/login_student/", methods = ("GET", "POST"))
@logged_out_required
def login_student():
    if request.method == "POST":
        roll_number = request.form["roll_number"]
        password = request.form["password"]
        user = Student.query.filter_by(roll_number = roll_number).first()
        if user is None:
            print("Student: {} doesn't exist".format(roll_number))
            return redirect(url_for("login_student"))
        elif not check_password_hash(user.password, password):
            print("Wrong password entered.")
            return redirect(url_for("login_student"))
        else:
            session.clear()
            session["type"] = "student"
            session["id"] = user.id
            session["roll_number"] = user.roll_number
            session["name"] = user.name
            session["email_id"] = user.email_id
            session["phone_number"] = user.phone_number
            session["cgpi"] = user.cgpi
            session["year"] = user.year
            print("Student: {} logged in.".format(user.name))
            return redirect(url_for("home_page"))
    else:
        return render_template("auth/login_student.html")


@app.route("/login_admin/", methods = ("GET", "POST"))
@logged_out_required
def login_admin():
    if request.method == "POST":
        user_name = request.form["user_name"]
        password = request.form["password"]
        user = Admin.query.filter_by(user_name = user_name).first()
        if user is None:
            print("Admin: {} doesn't exists.".format(user_name))
            return redirect(url_for("login_admin"))
        elif not check_password_hash(user.password, password):
            print("Wrong password entered")
            return redirect(url_for("login_admin"))
        else:
            session["type"] = "admin"
            session["name"] = user.user_name
            print("Admin: {} logged in.".format(user.user_name))
            return redirect(url_for("home_page"))
    else:
        return render_template("auth/login_admin.html")


@app.route("/logout/")
@logged_in_required
def logout():
    print("User: {} logged out".format(session["name"]))
    session.clear()
    return redirect(url_for("home_page"))
