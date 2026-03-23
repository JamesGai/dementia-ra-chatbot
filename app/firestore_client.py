import firebase_admin
from firebase_admin import credentials, firestore
import os
import json


def init_firestore():
    if not firebase_admin._apps:
        cred_json = (os.getenv("FIREBASE_CREDENTIALS_JSON") or "").strip()
        if cred_json:
            cred = credentials.Certificate(json.loads(cred_json))
        else:
            cred_path = os.getenv("FIREBASE_CREDENTIALS", "serviceAccountKey.json")
            cred = credentials.Certificate(cred_path)
        firebase_admin.initialize_app(cred)

    return firestore.client()
