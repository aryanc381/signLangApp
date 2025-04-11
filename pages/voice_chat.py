import os
import sys
import queue
import json
import sounddevice as sd
import numpy as np
import streamlit as st
from datetime import datetime
from vosk import Model, KaldiRecognizer

# Firestore config (adjust path to firebase_config.py)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from firebase_config import db

# === Configuration ===
MODEL_PATH = r"C:\Users\abdul\Desktop\webapp\pages\vosk-model-small-en-us-0.15"  # Adjust if needed
SAMPLE_RATE = 16000

# === Check Model ===
if not os.path.exists(MODEL_PATH):
    st.error("❌ Vosk model not found. Download and place it in the project folder.")
    st.stop()

model = Model(MODEL_PATH)
q = queue.Queue()

# === Page UI ===
st.set_page_config(page_title="🗣️ Voice Chat", page_icon="🎙", layout="centered")
st.title("🗣️ Interviewer Voice Chat")

# === Initialize session state ===
if "last_msg" not in st.session_state:
    st.session_state.last_msg = ""

# === Audio Callback ===
def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

# === Rule-based punctuation ===
def add_basic_punctuation(text):
    words = text.strip().split()
    if not words:
        return ""
    
    result = []
    sentence = []

    for i, word in enumerate(words):
        sentence.append(word)
        if (i + 1) % 8 == 0:
            result.append(" ".join(sentence).capitalize() + ".")
            sentence = []

    if sentence:
        result.append(" ".join(sentence).capitalize() + ".")

    return " ".join(result)

# === Record and Transcribe ===
def record_and_transcribe(duration=8):
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        st.info("🎙 Listening... Speak now.")
        rec = KaldiRecognizer(model, SAMPLE_RATE)
        result = ""

        for _ in range(0, int(SAMPLE_RATE / 8000 * duration)):
            data = q.get()
            if rec.AcceptWaveform(data):
                res = json.loads(rec.Result())
                result += res.get("text", "") + " "

        res = json.loads(rec.FinalResult())
        result += res.get("text", "")
        return result.strip()

# === UI Controls ===
st.subheader("🎤 Speak and Send Message")
duration = st.slider("Recording Duration", 5, 20, 8)

if st.button("Start Recording & Send"):
    transcription = record_and_transcribe(duration=duration)
    if transcription and transcription != st.session_state.last_msg:
        punctuated = add_basic_punctuation(transcription)

        # Save to Firestore
        db.collection("chat").add({
            "message": punctuated,
            "sender": "interviewer",
            "timestamp": datetime.utcnow()
        })

        st.session_state.last_msg = punctuated
        st.success("✅ Message sent to Interviewee")
        st.write(f"📤 Sent: **{punctuated}**")
    else:
        st.warning("No speech detected or message already sent.")

# === Display Messages from Interviewee ===
st.markdown("---")
st.subheader("💬 Live Chat (from Interviewee):")

messages = db.collection("chat").order_by("timestamp").stream()

for msg in messages:
    data = msg.to_dict()
    if data["sender"] == "interviewee":
        st.markdown(f"🧏 Interviewee: **{data['message']}**")
