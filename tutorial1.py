from flask import Flask, redirect , url_for, render_template , request, session, flash

# import for session lifetime 
from datetime import timedelta

app = Flask(__name__)
app.secret_key="hello"
# data saves for 5 minutes 
# if wanna save for 5 days do days=5 instead of minutes = 5

app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    return render_template("index.html" )

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        return redirect(url_for("user"))

    else:
        if "user" in session:
            return redirect(url_for("user"))
            
        return render_template("login.html")

@app.route("/user")
def user():
    if "user" in session:
        user = session["user"]
        return render_template("about.html" , usr = user)
    else:
        return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    # types of flashes warning , info , error
    flash("you have been loged out!", "info")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)

