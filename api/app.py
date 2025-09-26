import os
import json
import openai
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

# Firebase setup
cred_json = os.environ.get("FIREBASE_CREDENTIALS")
cred_dict = json.loads(cred_json)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

# OpenAI setup
openai.api_key = os.environ.get("OPENAI_API_KEY")

def generate_confession_image(confession_text):
    prompt = f"Create a stylish NGL-style Instagram post with the text: '{confession_text}'"
    response = openai.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="512x512"
    )
    image_url = response.data[0].url
    return image_url

# Confession submission
@app.route("/u/<username>", methods=["GET", "POST"])
def confession(username):
    if request.method == "POST":
        confession_text = request.form.get("message")
        image_url = generate_confession_image(confession_text)
        db.collection("messages").document().set({
            "username": username,
            "message": confession_text,
            "image": image_url
        })
        return redirect(url_for("dashboard", username=username))
    return render_template("confession_form.html", username=username)

# Dashboard
@app.route("/dashboard/<username>")
def dashboard(username):
    messages = db.collection("messages").where("username", "==", username).stream()
    messages_list = [{"text": m.to_dict()["message"], "image": m.to_dict()["image"]} for m in messages]
    return render_template("dashboard.html", messages=messages_list)

# Admin Panel
@app.route("/admin")
def admin():
    messages = db.collection("messages").stream()
    all_messages = [{"username": m.to_dict()["username"], "text": m.to_dict()["message"], "image": m.to_dict()["image"]} for m in messages]
    return render_template("admin.html", messages=all_messages)

if __name__ == "__main__":
    app.run(debug=True)
