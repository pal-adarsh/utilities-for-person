from flask import Flask, render_template, request, jsonify
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)

# Speech-to-Text API
@app.route('/speech-to-text', methods=['POST'])
def speech_to_text():
    recognizer = sr.Recognizer()
    audio_file = request.files['audio']
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        text = recognizer.recognize_google(audio_data)
        return jsonify({"text": text})
    except sr.UnknownValueError:
        return jsonify({"error": "Could not understand audio"})
    except sr.RequestError:
        return jsonify({"error": "Speech service error"})

# Text-to-Speech API
@app.route('/text-to-speech', methods=['POST'])
def text_to_speech():
    text = request.json.get("text", "")
    tts = gTTS(text=text, lang="en")
    filename = "static/audio/output.mp3"
    tts.save(filename)
    return jsonify({"audio_url": f"/{filename}"})

# Emergency Alert API
@app.route('/emergency-alert', methods=['POST'])
def emergency_alert():
    # Add logic to send alerts (e.g., email, SMS)
    return jsonify({"message": "Emergency alert sent to contacts!"})

# Home Route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    if not os.path.exists("static/audio"):
        os.makedirs("static/audio")
    app.run(debug=True)