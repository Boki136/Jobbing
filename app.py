import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index.html")
def homepage():

    return render_template("index.html")


@app.route("/register_jobseeker", methods=["GET", "POST"])
def register_jobseeker():

    if request.method == "POST":
        # do a check on a already existing username
        saved_user = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if saved_user:
            flash("Account with that email address already exists")
            return redirect(url_for("register_jobseeker"))

        register = {
            "first_name": request.form.get("fname"),
            "last_name": request.form.get("lname"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        # save the new user into "session"
        session["user"] = request.form.get("fname")
        return redirect(url_for('profile', user=session["user"]))

    return render_template("register-jobseeker.html")


@ app.route("/register_employer", methods=["GET", "POST"])
def register_employer():

    if request.method == "POST":
        # do a check on a already existing username
        saved_user = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if saved_user:
            flash("Account with that email address already exists")
            return redirect(url_for("register_employer"))

        register = {
            "first_name": request.form.get("fname"),
            "last_name": request.form.get("lname"),
            "email": request.form.get("email").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "company_name": request.form.get("company_name"),
            "company_address": request.form.get("company_address"),
            "is_employer": "Yes"
        }
        mongo.db.users.insert_one(register)

        # save the new user into "session"
        session["user"] = request.form.get("fname")
        return redirect(url_for('profile', user=session["user"]))

    return render_template("register-employer.html")


@ app.route("/profile/<user>", methods=["POST", "GET"])
def profile(user):

    # retrive users name from database
    user = mongo.db.users.find_one(
        {"first_name": session["user"]})["first_name"]

    if session["user"]:
        return render_template("profile.html", user=user)    

    return render_template("profile.html")


@ app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
