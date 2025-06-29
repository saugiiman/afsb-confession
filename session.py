from instagrapi import Client

USERNAME = "afsbconfession"
PASSWORD = "saugiiman04"

cl = Client()

# Try to login and save session
try:
    cl.login(USERNAME, PASSWORD)
    cl.dump_settings("session.json")
    print("✅ Logged in and session saved to session.json")
except Exception as e:
    print("❌ Login failed:", e)
