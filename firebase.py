import firebase_admin
from firebase_admin import credentials

# Only initialize once
if not firebase_admin._apps:
    cred = credentials.Certificate("api/secrets/firebase_service_key.json")
    firebase_admin.initialize_app(cred)
