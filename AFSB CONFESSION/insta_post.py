from instagrapi import Client
import os

def post_to_instagram(image_path, caption):
    cl = Client()

    # Load existing session if available
    if os.path.exists("session.json"):
        cl.load_settings("session.json")
        try:
            cl.login("afsbconfession", "saugiiman04")
        except Exception as e:
            print("⚠️ Login with session failed, retrying:", e)
            cl.login("afsbconfession", "saugiiman04")
            cl.dump_settings("session.json")
    else:
        cl.login("afsbconfession", "saugiiman04")
        cl.dump_settings("session.json")

    cl.photo_upload(image_path, caption)
    print("✅ Posted to Instagram!")
