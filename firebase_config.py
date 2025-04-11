import firebase_admin
from firebase_admin import credentials, firestore
import streamlit as st
import json
import os

# Load Firebase Web API Key from Streamlit Secrets or environment variable
WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY") or st.secrets["FIREBASE_WEB_API_KEY"]

if not WEB_API_KEY:
    raise ValueError("Firebase Web API Key not found. Ensure it's set in Streamlit secrets or as environment variable.")

# Initialize Firebase Admin SDK using credentials from Streamlit Secrets
if not firebase_admin._apps:
    firebase_credentials_json = st.secrets["FIREBASE_ADMIN_CREDENTIALS"]
    cred_dict = json.loads(firebase_credentials_json)
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred)

# Firestore DB Client
db = firestore.client()
