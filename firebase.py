import firebase_admin
from firebase_admin import credentials

# Only initialize once
if not firebase_admin._apps:
    cred = credentials.Certificate("api/secrets/mockt-interview-prep-firebase-adminsdk-fbsvc-4ed1a112cc.json")
    firebase_admin.initialize_app(cred)
