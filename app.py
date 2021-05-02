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
            return redirect(url_for("register_jobseeker",
                                    _external=True, _scheme='https'))

        register = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "is_jobseeker": "Yes",
            "saved_jobs": [],
        }
        mongo.db.users.insert_one(register)

        # save the new user into "session"
        session["user"] = request.form.get("email")
        return redirect(url_for('profile', user=session["user"],
                                _external=True, _scheme='https'))

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
            return redirect(url_for("register_employer",
                                    _external=True, _scheme='https'))

        register = {
            "name": request.form.get("name"),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password")),
            "company_name": request.form.get("company_name"),
            "company_address": request.form.get("company_address"),
            "is_employer": "Yes",
            "posted_jobs": [],
        }
        mongo.db.users.insert_one(register)

        # save the new user into "session"
        session["user"] = request.form.get("email")
        return redirect(url_for('profile', user=session["user"],
                                _external=True, _scheme='https'))

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
                'profile', user=session["user"],
                _external=True, _scheme='https'))
        else:
            # username doesn't exists
            flash("Invalid username and/or password")
            return redirect(url_for("login",
                                    _external=True, _scheme='https'))

    return render_template("login.html")


@ app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login",
                            _external=True, _scheme='https'))


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
            return redirect(url_for("profile",
                                    _external=True, _scheme='https'))

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
            return redirect(url_for("profile",
                                    _external=True, _scheme='https'))

    # Check if user is jobseeker or employer and show relevent info

    try:
        user["is_jobseeker"]
    except:
        KeyError
    else:
        saved_jobs = user["saved_jobs"]

        return render_template("profile.html", user=user,
                               saved_jobs=saved_jobs)

    try:
        user["is_employer"]

    except:
        KeyError

    else:
        posted_jobs = user["posted_jobs"]
        return render_template("profile.html", user=user,
                               posted_jobs=posted_jobs)

    return redirect(url_for("login",
                            _external=True, _scheme='https'))


@ app.route("/post_job", methods=["GET", "POST"])
def post_job():

    # check if user is logged in and send them to correct page
    try:
        # retrive users name from database
        user = mongo.db.users.find_one(
            {"email": session["user"]})
    except:
        KeyError
        flash("Sign In to post jobs")
        return redirect(url_for('login',
                                _external=True, _scheme='https'))

        # check if user is employer and allow job posting
    try:
        user["is_employer"]
    except:
        KeyError
    else:
        company_name = str(user["company_name"])
        company_address = str(user["company_address"])

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
            mongo.db.users.update_one(
                {"_id": user["_id"]},
                {"$push": {"posted_jobs": new_job}}
            )
            flash("Job Posted Successfully")
            return redirect(url_for("post_job",
                                    _external=True, _scheme='https'))

    # check if user is jobseeker and don't allow job posting
    try:
        user["is_jobseeker"]
    except:
        KeyError
    else:
        flash("Register as employer to post jobs")
        return redirect(url_for("register_employer",
                                _external=True, _scheme='https'))

    return render_template('post_job.html')


@ app.route("/find-job", methods=["GET", "POST"])
def find_job():

    all_jobs = list(mongo.db.jobs.find())

    try:
        # retrive users name from database
        user = mongo.db.users.find_one(
            {"email": session["user"]})
    except:
        KeyError

        if KeyError:
            return render_template('find_job.html', all_jobs=all_jobs)
        else:
            pass

    if request.method == "POST":
        job_category = request.form.get("job_category_name")
        all_jobs = list(mongo.db.jobs.find({
            "job_category": job_category}))
        return render_template('find_job.html',
                               all_jobs=all_jobs, job_category=job_category)

    return render_template('find_job.html',
                           all_jobs=all_jobs, user=user)


@ app.route("/find-job-mobile", methods=["GET", "POST"])
def find_job_mobile():

    all_jobs = list(mongo.db.jobs.find())

    try:
        # retrive users name from database
        user = mongo.db.users.find_one(
            {"email": session["user"]})
    except:
        KeyError

        if KeyError:
            return render_template('find_job.html', all_jobs=all_jobs)
        else:
            pass

    if request.method == "POST":
        job_category = request.form.get("job_category_name")
        all_jobs = list(mongo.db.jobs.find({
            "job_category": job_category}))
        return render_template('find_job_mobile.html',
                               all_jobs=all_jobs, job_category=job_category)

    return render_template('find_job_mobile.html',
                           all_jobs=all_jobs, user=user)


@ app.route("/save-job", methods=["GET", "POST"])
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
        saved_jobs = user["saved_jobs"]

        # do a check if a job is already saved
        if saved_job not in saved_jobs:

            flash("Job saved successfully")
            # update saved_jobs record
            mongo.db.users.update_one(
                {"_id": user["_id"]},
                {"$push": {"saved_jobs": saved_job}}
            )
        else:
            flash("Job already saved")
            return redirect(url_for('find_job', _anchor='job-listing-wrap',
                                    _external=True, _scheme='https'))

        return redirect(url_for("find_job", _anchor='job-listing-wrap',
                                _external=True, _scheme='https'))


@ app.route("/save-job-mobile", methods=["GET", "POST"])
def save_job_mobile():

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
        saved_jobs = user["saved_jobs"]

        # do a check if a job is already saved
        if saved_job not in saved_jobs:

            flash("Job saved successfully")
            # update saved_jobs record
            mongo.db.users.update_one(
                {"_id": user["_id"]},
                {"$push": {"saved_jobs": saved_job}}
            )
        else:
            flash("Job already saved")
            return redirect(url_for('find_job_mobile',
                                    _anchor='job-listing-wrap',
                                    _external=True, _scheme='https'))

        return redirect(url_for("find_job_mobile",
                                _anchor='job-listing-wrap',
                                _external=True, _scheme='https'))


@ app.route("/edit_job/<post>", methods=["GET", "POST"])
def edit_job(post):

    # retrive users name from database
    user = mongo.db.users.find_one(
        {"email": session["user"]})

    # retrive job from profile page
    job = mongo.db.jobs.find_one({
        "_id": ObjectId(post)
    })

    if request.method == "POST":

        # remove the old version of the saved job from user collection
        mongo.db.users.update(
            {"_id": user["_id"]},
            {"$pull": {"posted_jobs": {"_id": ObjectId(post)}}}
        )

        # update the selected job
        update_job = {"$set": {
            "job_title": request.form.get("job_title"),
            "job_description": request.form.get("job_description"),
            "salary_range": request.form.get("salary_range"),
        }}

        mongo.db.jobs.update_one(job, update_job)

        flash("Job changed Sucessfully")
        return redirect(url_for('edit_job', post=post,
                                _external=True, _scheme='https'))

    # check if the job is already saved, add the job id not existing
    saved_jobs = user["posted_jobs"]
    if job in saved_jobs:
        pass
    elif job not in saved_jobs:
        mongo.db.users.update(
            {"_id": user["_id"]},
            {"$push": {"posted_jobs": job}}
        )
    return render_template('edit_job.html', post=post, job=job)


@ app.route("/delete_saved_job", methods=["GET", "POST"])
def delete_saved_job():

    # retrive users name from database
    user = mongo.db.users.find_one(
        {"email": session["user"]})

    if request.method == "POST":

        # retrive id from submitted job for jobseeker and employer
        job_id = request.form.get("job_id")
        post_id = request.form.get("post_id")

        # find job by job_id jobseeker & update the array in db
        deleted_job_jobseeker = mongo.db.jobs.find_one(
            {
                "_id": ObjectId(job_id)
            }
        )

        mongo.db.users.update_one(
            {"_id": user["_id"]},
            {"$pull": {"saved_jobs": deleted_job_jobseeker}}
        )

        # find job by job_id employer & update the array in db
        deleted_job_employer = mongo.db.jobs.find_one(
            {
                "_id": ObjectId(post_id)
            }
        )
        mongo.db.users.update_one(
            {"_id": user["_id"]},
            {"$pull": {"posted_jobs": deleted_job_employer}}
        )

        # remove a job from jobs collection
        mongo.db.jobs.remove({
            "_id": ObjectId(post_id)
        })

        flash("Job deleted successfully")

        return redirect(url_for("profile",
                                _external=True, _scheme='https'))


@ app.route("/contact")
def contact():

    return render_template("contact.html")


@ app.route("/search", methods=["POST", "GET"])
def search():

    search_term = request.form.get("search_box")
    all_jobs = list(mongo.db.jobs.find({"$text": {"$search": search_term}}))

    return render_template('find_job.html',
                           all_jobs=all_jobs)


@ app.route("/search_mobile", methods=["POST", "GET"])
def search_mobile():

    search_term = request.form.get("search_box")
    all_jobs = list(mongo.db.jobs.find({"$text": {"$search": search_term}}))

    return render_template('find_job_mobile.html',
                           all_jobs=all_jobs)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
