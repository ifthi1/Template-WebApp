from flask import Flask, g, render_template, request, flash, redirect, url_for, flash, g
import os
import sqlite3
import secrets
import json
import datetime
from datetime import datetime
import sqlite3
from flask_login import current_user, login_required, login_user, UserMixin, LoginManager, logout_user
import werkzeug

app = Flask(__name__)
app.secret_key = secrets.token_hex(16) # This is necessary for flash!

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = name
        self.user_id = id
        self.name = name
        self.password = password

@login_manager.user_loader
def user_loader(name):
    record = get_db().execute("SELECT id, username, password FROM Users WHERE username = ? LIMIT 1", [name]).fetchone()
    if not record:
        return None
    return User(record[0], record[1], record[2])

path = "users.db" 
database_exists = os.path.isfile(path)
db = sqlite3.connect("users.db")
if not database_exists: 
    db.execute("CREATE TABLE Users (id INTEGER PRIMARY KEY AUTOINCREMENT, username VARCHAR(255), password VARCHAR(32))")
    db.execute("INSERT INTO Users (username, password) VALUES('Ifthi', '1234')")
    db.execute("INSERT INTO Users (username, password) VALUES('John', '4321')")
    db.commit()


# Gets a database connection.
def get_db():
  db = g.get("_database")
  if not db:
    db = sqlite3.connect("chat.db")
    g._database = db
  return db

@app.route("/login")
def login_form():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    name = request.form["username"]
    password = request.form["password"]
    record = get_db().execute("SELECT id, password FROM Users WHERE username = ? LIMIT 1", [name]).fetchone()
    print("Record: ",record)
    if not record or password != record[1]:
        print("Record: ",record)
        flash("Login info invalid!!!")
        return redirect(url_for("login_form"))
    user = User(record[0], name, record[1])
    login_user(user)
    return redirect(url_for("home"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))
  
@app.route("/")
@login_required
def home():
  return render_template("home.html")

# Cleans up a database connection.
@app.teardown_appcontext
def cleanup(exception):
  db = g.get("_database")
  if db:
    db.close()
