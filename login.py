from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
import hashlib
app = Flask(__name__)
app.secret_key = "your_secret_key"  # Change this to a secret key
# Database configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678",
    database="students"
)
@app.route('/')
def start():
    return render_template('login.html')
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    print(username,password)
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    if result is not None:
        stored_password = result[0]
        if password == stored_password:
            session["username"] = username
            flash("Login successful", "success")
            return redirect(url_for("welcome"))
    
    flash("Login failed. Check your username and password.", "error")
    return redirect(url_for("start"))

@app.route("/welcome")
def welcome():
    return render_template('welcome.html')
    if "username" in session:
        return f"Welcome, {session['username']}!"
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)