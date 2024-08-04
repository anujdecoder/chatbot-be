# This file handles the configuration and initialization of config services
import firebase_admin

from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("keys.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
