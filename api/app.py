from flask import Flask, render_template, request, redirect, url_for, session
import firebase_admin
from firebase_admin import credentials, firestore

# ---------------- Flask setup ----------------
app = Flask(__name__, template_folder="../templates", static_folder="../static")
app.secret_key = "supersecretkey"  # for admin login

# ---------------- Firebase setup ----------------
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# ---------------- Routes ----------------

# Landing page
@app.route("/")
def home():
    return render_template("index.html")

# Confession form page
@app.route("/u/<username>", methods=["GET", "POST"])
def confession(username):
    if request.method == "POST":
        msg = request.form.get("message")
        if msg:
            db.collection("messages").document().set({
                "username": username,
                "content": msg
            })
            return render_template("confession.html", username=username, success=True)
    return render_template("confession.html", username=username, success=False)

# User dashboard
@app.route("/dashboard/<username>")
def dashboard(username):
    msgs = db.collection("messages").where("username", "==", username).stream()
    messages = [m.to_dict()["content"] for m in msgs]
    return render_template("dashboard.html", username=username, messages=messages)

# Admin login
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        user = request.form.get("username")
        pwd = request.form.get("password")
        if user == "saugiiman" and pwd == "saugiiman04":
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("admin_login.html", error="Invalid credentials")
    return render_template("admin_login.html", error=None)

# Admin dashboard
@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    msgs = db.collection("messages").stream()
    messages = [(m.to_dict()["username"], m.to_dict()["content"]) for m in msgs]
    return render_template("admin_dashboard.html", messages=messages)

# Admin logout
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect(url_for("admin_login"))

if __name__ == "__main__":
    app.run(debug=True)
