from flask import Flask, redirect , url_for, render_template , request, session, flash

# import for session lifetime 
from datetime import timedelta

# sqlalchemy import for DB 
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key="hello"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# data saves for 5 minutes 
# if wanna save for 5 days do days=5 instead of minutes = 5


app.permanent_session_lifetime = timedelta(minutes=5)


# this is the database object 
db = SQLAlchemy(app)

class users(db.Model):
    _id = db.Column("id",db.Integer,primary_key = True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, name , email):
        self.name = name
        self.email = email

@app.route("/")
def home():
    return render_template("index.html" )

@app.route("/view")
def view():
    # users.query.all() gets all data of users and  render them into the template where we can display the data
    return render_template("view.html", values=users.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user

        found_user = users.query.filter_by(name=user).first()
        if found_user:
            session["email"] = found_user.email

        else:
            usr = users(user, "")
            db.session.add(usr)
            # commit every time changes are made 
            db.session.commit()

        flash("Login sucessful!")
        return redirect(url_for("user"))

    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("user"))
            
        return render_template("login.html")

@app.route("/user", methods= ["POST","GET"])
def user():
    email = None

    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = users.query.filter_by(name=user).first()
            found_user.email = email
            db.session.commit()
            flash("email was saved")
        
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html" , email = email)
    else:
        flash("you are not logged in")
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash("you have been logged out!", "info")
    session.pop("user", None)
    session.pop("email", None)
    # types of flashes warning , info , error
    return redirect(url_for("login"))

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)

