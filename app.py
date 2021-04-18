import os
from datetime import datetime, timedelta
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
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "is_jobseeker": "Yes",
        }
        mongo.db.users.insert_one(register)

        # save the new user into "session"
        session["user"] = request.form.get("email")
        return redirect(url_for('profile', user=session["user"]))

    return render_template("register-jobseeker.html")


@ app.route("/register_employer", methods=["GET", "POST"])
def register_employer():

    if request.method == "POST":
        # do a check on a already existing username
        saved_user = mongo.db.users.find_one(
            {"email": request.form.get("email")})

        if saved_user:
            flash(
                "Account with that email address already exists, please Sign In"
            )
            return redirect(url_for("register_employer"))

        register = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "company_name": request.form.get("company_name"),
            "company_address": request.form.get("company_address"),
            "is_employer": "Yes",
        }
        mongo.db.users.insert_one(register)

        # save the new user into "session"
        session["user"] = request.form.get("email")
        return redirect(url_for('profile', user=session["user"]))

    return render_template("register-employer.html")


def is_user_authorised():
    # do a check on existing user
    existing_user = mongo.db.users.find_one(
        {"email": request.form.get("email")})
    if existing_user:
        # chek if the passowrd matches user input
        if check_password_hash(
                existing_user["password"], request.form.get("password")):
            session["user"] = request.form.get("email")
            return session
        else:
            return None
    else:
        return None


@ app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # do a check on existing user
        session = is_user_authorised()
        if session:
            return redirect(url_for(
                'profile', user=session["user"]))
        else:
            # username doesn't exists
            flash("Invalid username and/or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@ app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@ app.route("/profile", methods=["GET", "POST"])
def profile():

    # retrive users name from database
    user = mongo.db.users.find_one(
        {"email": session["user"]})

    employer = request.form.get("employer_name")
    jobseeker = request.form.get("jobseeker_name")

    if request.method == "POST":
        if employer:

            submit = {
                "name": employer,
                "email": user["email"],
                "password": user["password"],
                "company_name": user["company_name"],
                "company_address": user["company_address"],
                "is_employer": "Yes",

            }

            mongo.db.users.update(
                {"_id": user["_id"]}, submit)
            return redirect(url_for("profile"))

        elif jobseeker:
            submit = {
                "name": jobseeker,
                "email": user["email"],
                "password": user["password"],
                "is_jobseeker": "Yes",
                "saved_jobs": user["saved_jobs"],
            }

            mongo.db.users.update(
                {"_id": user["_id"]}, submit)
            return redirect(url_for("profile"))

    if session["user"]:

        saved_jobs_array = mongo.db.users.distinct(
            "saved_jobs"
        )

        return render_template("profile.html", user=user,
                               saved_jobs_array=saved_jobs_array)

    return redirect(url_for("login"))


@ app.route("/post_job", methods=["GET", "POST"])
def post_job():

    # retrive users name from database
    users = mongo.db.users.find_one(
        {"email": session["user"]})

    company_name = str(users["company_name"])
    company_address = str(users["company_address"])

    posted_date = datetime.now().date()
    if request.method == "POST":

        new_job = {
            "job_title": request.form.get("job_title"),
            "job_category": request.form.get("job_category"),
            "contract_type": request.form.get("contract_type"),
            "job_description": request.form.get("job_description"),
            "salary_range": request.form.get("salary_range"),
            "posted_date": posted_date.strftime("%d/%m/%y"),
            "company_name": company_name,
            "company_address": company_address,
        }

        mongo.db.jobs.insert_one(new_job)
        flash("Job Posted Successfully")
        return redirect(url_for("post_job"))

    return render_template('post_job.html')


@ app.route("/find-job", methods=["GET", "POST"])
def find_job():

    all_jobs = list(mongo.db.jobs.find())

    return render_template('find_job.html', all_jobs=all_jobs)


@ app.route("/find-job-mobile")
def find_job_mobile():

    all_jobs = list(mongo.db.jobs.find())

    return render_template('find_job_mobile.html', all_jobs=all_jobs)


@app.route("/save-job", methods=["GET", "POST"])
def save_job():

    # retrive users name from database
    user = mongo.db.users.find_one(
        {"email": session["user"]})

    if request.method == "POST":

        # retrive id from subbmited job
        job_id = request.form.get("job_id")

        # find job by job_id
        saved_job = mongo.db.jobs.find_one(
            {
                "_id": ObjectId(job_id)
            }
        )

        # save all records from saved_jobs
        saved_jobs_array = mongo.db.users.distinct(
            "saved_jobs"
        )

        # do a check if a job is already saved
        if saved_job not in saved_jobs_array:

            flash("Job saved successfully")
            # update saved_jobs record
            mongo.db.users.update_one(
                {"_id": user["_id"]},
                {"$push": {"saved_jobs": saved_job}}
            )
        else:
            flash("Job already saved")
            return redirect(url_for('find_job'))

        # retrive all saved jobs
        saved_jobs_array = mongo.db.users.distinct(
            "saved_jobs"
        )

        return redirect(url_for("find_job"))


@app.route("/delete_saved_job", methods=["GET", "POST"])
def delete_saved_job():

    # retrive users name from database
    user = mongo.db.users.find_one(
        {"email": session["user"]})

    if request.method == "POST":

        # retrive id from subbmited job
        job_id = request.form.get("job_id")
        print(job_id)

        # find job by job_id
        deleted_job = mongo.db.jobs.find_one(
            {
                "_id": ObjectId(job_id)
            }
        )

        # save all records from saved_jobs
        saved_jobs_array = mongo.db.users.distinct(
            "saved_jobs"
        )

        mongo.db.users.update_one(
            {"_id": user["_id"]},
            {"$pull": {"saved_jobs": deleted_job}}
        )

        flash("Job deleted successfully")

        return redirect(url_for("profile"))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
