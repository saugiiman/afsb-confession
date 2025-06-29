from flask import Flask, render_template, request, redirect, flash
from image_gen import create_confession_image
from caption_gen import generate_caption
from insta_post import post_to_instagram
from datetime import datetime
import uuid
import os
import threading

app = Flask(__name__)
app.secret_key = "secret-key"  # Needed for flashing messages

os.makedirs("generated", exist_ok=True)

def save_to_file(confession, request):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user_ip = request.remote_addr or "Unknown IP"
    with open("confessions.txt", "a", encoding="utf-8") as file:
        file.write(f"[{timestamp}] (IP: {user_ip})\n")
        file.write(confession.strip() + "\n\n")

def background_post(confession, filename):
    create_confession_image(confession, filename)
    caption = generate_caption(confession)
    post_to_instagram(filename, caption)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    confession = request.form.get("confession", "").strip()

    if not confession or len(confession) < 5:
        return "Confession too short. Please type at least 5 characters.", 400

    save_to_file(confession, request)
    filename = f"generated/{uuid.uuid4().hex}.png"

    # Start background thread
    threading.Thread(target=background_post, args=(confession, filename)).start()

    # Fast response
    return render_template("success.html")

if __name__ == "__main__":
    app.run(debug=True)
