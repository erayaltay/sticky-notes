import datetime
import os
import hashlib
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv
from bson.objectid import ObjectId

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.secret_key = "super secret key"

    # MongoDB connection
    client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = client.eray

    class Users:
        def __init__(self, email: str, name: str, password: str):
            self.email = email
            self.name = name
            self.password = password

    # function to hash string with SHA256
    def hash(raw_text: str):
        return hashlib.sha256(raw_text.encode()).hexdigest()
        
    @app.route("/")
    def default_page():
        return redirect(url_for("login"))

    @app.route("/notes/", methods=["GET", "POST"])
    def notes():
        if request.method == "POST":
            new_request = request.get_json()

            if new_request["action"] == "create":
                app.db.notes.insert_one({
                    "noteTitle": new_request["noteTitle"],
                    "noteContent": new_request["noteContent"]
                })
                return redirect(url_for("notes"))
            
            elif new_request["action"] == "delete":
                app.db.notes.delete_one({
                    "_id" : ObjectId(new_request["noteId"])
                })
                return redirect(url_for("notes"))
            
            elif new_request["action"] == "save":
                # filter over the primary key(s)
                filter = {
                    '_id': ObjectId(new_request["noteId"])
                }
                # values to be updated
                sticky_note_content = {
                    "$set": {
                        "noteTitle": new_request["noteTitle"],
                        "noteContent": new_request["noteContent"]
                    }
                }
                # update the record
                app.db.notes.update_one(filter, sticky_note_content)
                return redirect(url_for("notes"))

        saved_notes = [
            (   
                note["noteTitle"],
                note["noteContent"],
                str(note["_id"])
            )
            for note in app.db.notes.find({})
        ]
        kwargs = {
            "notes": saved_notes
        }
        return render_template("notes.html", **kwargs)
        
    @app.route("/login/")
    def login():
        return render_template("login.html")

    @app.route("/login/", methods=["GET", "POST"])
    def login_user():
        if request.method == "POST":
            # get user's email address from the login page and convert the letters to lowercase
            user_email = request.form.get("email").lower()
            hashed_user_email = hash(user_email)
            # get user's password from the login page
            user_password = request.form.get("password")
            hashed_user_password = hash(user_password)

            # loop through the users
            for user in app.db.users.find({}):
                if user["email"] == hashed_user_email and user["password"] == hashed_user_password:
                    # redirect to notes page
                    return redirect(url_for("notes"))
                else:
                    # show error message
                    flash("Invalid email or password!")
                    return redirect(url_for("login"))
    
    @app.route("/signup/")
    def signup():
        return render_template("signup.html")

    @app.route("/signup/", methods=["GET", "POST"])
    def signup_user():
        if request.method == "POST":
            # get user's name from the sign up form
            new_user_name = request.form.get("name").lower()
            # get user's email address from the sign up form and convert the letters to lowercase
            new_user_email = request.form.get("email").lower()
            hashed_user_email = hash(new_user_email)
            # get user's password from the sign up form
            new_user_password = request.form.get("password")

            # loop through the users
            for user in app.db.users.find({}):
                if user["email"] == hashed_user_email:
                    # show that the account already exists to the user
                    flash("You already have an account.")
                    return redirect(url_for("signup"))
                else:
                    # save the user's credentials to MongoDB
                    app.db.users.insert_one({
                        "name": new_user_name,
                        "email": hash(new_user_email),
                        "password": hash(new_user_password)
                    })
                    # show success message to the user
                    flash("You signed up!")
                    return redirect(url_for("signup"))
        return render_template("signup.html")
    
    return app