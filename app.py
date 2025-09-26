from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

# ---------------------------
# Database setup
# ---------------------------
DB_NAME = "messages.db"

def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """)
        conn.commit()
        conn.close()

init_db()

# ---------------------------
# Routes
# ---------------------------

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
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute("INSERT INTO messages (username, content) VALUES (?, ?)", (username, msg))
            conn.commit()
            conn.close()
            return "✅ Message sent! <a href='/u/{}'>Back</a>".format(username)
    return render_template("confession.html", username=username)

# Dashboard to view messages
@app.route("/dashboard/<username>")
def dashboard(username):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT content FROM messages WHERE username = ?", (username,))
    messages = [row[0] for row in c.fetchall()]
    conn.close()
    return render_template("dashboard.html", username=username, messages=messages)

if __name__ == "__main__":
    app.run(debug=True)
