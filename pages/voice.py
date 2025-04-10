import os
import queue
import sounddevice as sd
import json
import numpy as np
import streamlit as st
from vosk import Model, KaldiRecognizer

# === Configuration ===
MODEL_PATH = r"C:\Users\conta\Desktop\Web\vosk-model-small-en-us-0.15"  # Replace with your actual path
SAMPLE_RATE = 16000

# === Load Model ===
if not os.path.exists(MODEL_PATH):
    st.error("❌ Vosk model not found. Download and place it in the project folder.")
    st.stop()

model = Model(MODEL_PATH)
q = queue.Queue()

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
        # Add period after every ~8 words (basic heuristic)
        if (i + 1) % 8 == 0:
            result.append(" ".join(sentence).capitalize() + ".")
            sentence = []

    # Add remaining sentence
    if sentence:
        result.append(" ".join(sentence).capitalize() + ".")

    return " ".join(result)

# === Record and Transcribe ===
def record_and_transcribe(duration=10):
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

# === Streamlit UI ===
st.set_page_config(page_title="Voice to Text", page_icon="🎙", layout="centered")
st.title("🎙 Interview System (Fast)")

duration = st.slider("Recording Duration (seconds)", 5, 20, 10)

if st.button("Start Recording"):
    transcription = record_and_transcribe(duration=duration)
    if transcription:
        st.subheader("🔤 Raw Transcription")
        st.markdown(transcription)

        punctuated = add_basic_punctuation(transcription)
        st.subheader("📝 Punctuated Text")
        st.markdown(punctuated)
    else:
        st.warning("No speech detected. Try again.")
