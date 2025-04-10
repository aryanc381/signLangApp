import streamlit as st
import cv2
import numpy as np
import mediapipe as mp
from keras.models import load_model
import requests
import pyttsx3
import time
import os

# 🔒 Authentication Check
if "username" not in st.session_state:
    st.warning("Please login to access the app.")
    st.switch_page("main.py")

# Page Settings
st.set_page_config(
    page_title="Sign Language Detection",
    page_icon="🤟",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.sidebar .sidebar-content {
    background-color: #f0f2f6;
}
[data-testid="stSidebar"] {
    min-width: 300px;
    max-width: 300px;
}
</style>
""", unsafe_allow_html=True)

st.title("Sign Language Detection")
st.success(f"Welcome, {st.session_state['username']}!")
st.markdown("---")

# Initialize MediaPipe
mp_holistic = mp.solutions.holistic
mp_drawing = mp.solutions.drawing_utils 

# Load model
try:
    model_path = os.path.join(os.path.dirname(__file__), "best_model_withGPU3.h5")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    model = load_model(model_path)
    actions = np.array(['hello', 'mandar', 'language', 'my', 'name', 'i', 'internet', 'computer', 'data-entry', 'one', 'please'])
except Exception as e:
    st.error(f"Error loading model: {str(e)}")
    st.stop()

# Text-to-speech
def speak_text(text):
    try:
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        st.error(f"Speech failed: {e}")

# Grammar correction using DeepSeek
def correct_grammar_with_deepseek(text):
    prompt = (
        f"Correct the grammar of this sentence and complete it: \"{text}\".\n"
        "Only reply with the corrected sentence. No other explanation."
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "deepseek-llm",
                "prompt": prompt,
                "stream": False
            }
        )
        if response.status_code == 200:
            return response.json()["response"].strip().strip('"\n ')
        else:
            return text
    except:
        return text

# Session state init
for key in ['sequence', 'sentence', 'webcam_active', 'final_sentence']:
    if key not in st.session_state:
        st.session_state[key] = [] if key not in ['webcam_active', 'final_sentence'] else False if key == 'webcam_active' else ""

# Sidebar controls
with st.sidebar:
    st.header("Settings")
    st.slider("Detection Threshold", 0.1, 1.0, 0.7, key="threshold")
    if st.button("🔄 Reset Session"):
        st.session_state.sequence = []
        st.session_state.sentence = []
        st.session_state.final_sentence = ""
        st.rerun()
    if st.button("← Back to Home"):
        st.session_state.webcam_active = False
        st.switch_page("main.py")

# Keypoint extractor
def extract_keypoints(results):
    pose = np.array([[res.x, res.y, res.z, res.visibility] for res in results.pose_landmarks.landmark]).flatten() if results.pose_landmarks else np.zeros(33*4)
    face = np.array([[res.x, res.y, res.z] for res in results.face_landmarks.landmark]).flatten() if results.face_landmarks else np.zeros(468*3)
    lh = np.array([[res.x, res.y, res.z] for res in results.left_hand_landmarks.landmark]).flatten() if results.left_hand_landmarks else np.zeros(21*3)
    rh = np.array([[res.x, res.y, res.z] for res in results.right_hand_landmarks.landmark]).flatten() if results.right_hand_landmarks else np.zeros(21*3)
    return np.concatenate([pose, face, lh, rh])

# Sentence update
def update_sentence(new_action):
    if len(st.session_state.sentence) == 0 or new_action != st.session_state.sentence[-1]:
        st.session_state.sentence.append(new_action)
    if len(st.session_state.sentence) > 5:
        st.session_state.sentence = st.session_state.sentence[-5:]

# Draw prediction probs
def display_probabilities(image, res, actions):
    for i, (action, prob) in enumerate(zip(actions, res)):
        cv2.putText(image, f"{action}: {prob:.2f}", (10, 30+i*30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

# Main app
def main_app():
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Live Detection")
        run = st.checkbox('Start Webcam', key='webcam')
        FRAME_WINDOW = st.image([])

    with col2:
        st.subheader("Instructions")
        st.info("""
        1. Click 'Start Webcam'
        2. Show these signs:
           - 👋 Hello
           - 🤝 Mandar
           - 🗣️ Language
           - 👤 My
           - 📛 Name
           - 👈 I
           - 🌐 Internet
           - 💻 Computer
           - 📊 Data-entry
           - 1️⃣ One
           - 🙏 Please
        """)
        st.markdown("---")
        st.subheader("Detected Signs")
        DETECTION_WINDOW = st.empty()

    cap = None
    if run:
        cap = cv2.VideoCapture(0)
        st.session_state.webcam_active = True

    frame_count = 0
    max_frames = 500  # limit to avoid infinite loop in Streamlit

    while run and st.session_state.webcam_active and frame_count < max_frames:
        ret, frame = cap.read()
        frame_count += 1
        if not ret:
            st.error("Webcam error")
            break
        
        with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
            try:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = holistic.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                # Draw landmarks
                mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACE_CONNECTIONS)
                mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS)
                mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS)

                # Extract keypoints
                keypoints = extract_keypoints(results)
                st.session_state.sequence.append(keypoints)
                st.session_state.sequence = st.session_state.sequence[-30:]

                # Predict
                if len(st.session_state.sequence) == 30:
                    res = model.predict(np.expand_dims(st.session_state.sequence, axis=0))[0]

                    if res[np.argmax(res)] > st.session_state.threshold:
                        update_sentence(actions[np.argmax(res)])

                    DETECTION_WINDOW.success(f"*Detected:* {' '.join(st.session_state.sentence)}")
                    display_probabilities(image, res, actions)

                FRAME_WINDOW.image(image, channels="BGR")

            except Exception as e:
                st.error(f"Processing error: {str(e)}")
                break

    if cap:
        cap.release()

    # If a sentence was detected
    if len(st.session_state.sentence) >= 3:
        raw_sentence = ' '.join(st.session_state.sentence)
        corrected = correct_grammar_with_deepseek(raw_sentence)
        st.session_state.final_sentence = corrected
        st.info(f"✅ Interviewee said {corrected}")
        speak_text(corrected)
        st.session_state.sentence = []

# Run the app
if __name__ == "__main__":
    main_app()
