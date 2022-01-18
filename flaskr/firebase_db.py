import os
import firebase_admin
from firebase_admin import credentials

GOOGLE_APPLICATION_CREDENTIALS = "midyear-circle-337709-3749a3c5b159.json"


def connect_firebase():
    """
    Use a service account
    """
    PROJECT_BASE_PATH = os.path.dirname(os.path.dirname(__file__))

    cred = credentials.Certificate(
        os.path.join(PROJECT_BASE_PATH, GOOGLE_APPLICATION_CREDENTIALS)
    )
    firebase_admin.initialize_app(cred)
