from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import speech_recognition as sr
from gtts import gTTS
import os

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Dummy user database
users = {"user1": "password1"}
users = {"binita": "binita1"}

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin):
    pass

@login_manager.user_loader
def load_user(username):
    if username in users:
        user = User()
        user.id = username
        return user
    return None

# Login Route
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users and users[username] == password:
        user = User()
        user.id = username
        login_user(user)
        return jsonify({"success": True})
    else:
        return jsonify({"success": False, "message": "Invalid credentials"})

# User Type Selection Route
@app.route("/select-user-type", methods=["POST"])
@login_required
def select_user_type():
    data = request.json
    user_type = data.get("userType")
    return jsonify({"success": True})

# Home Route
@app.route("/")
@login_required
def index():
    return render_template("index.html")

# Speech-to-Text Route
@app.route("/speech-to-text")
@login_required
def speech_to_text_page():
    return render_template("speech_to_text.html")

# Text-to-Speech Route
@app.route("/text-to-speech")
@login_required
def text_to_speech_page():
    return render_template("text_to_speech.html")

# Audio Notes Route
@app.route("/audio-notes")
@login_required
def audio_notes_page():
    return render_template("audio_notes.html")

# Sign Language Route
@app.route("/sign-language")
@login_required
def sign_language_page():
    return render_template("sign_language.html")

# To-Do List Route
@app.route("/todo")
@login_required
def todo_page():
    return render_template("todo.html")

# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login_page"))

# Login Page Route
@app.route("/login-page")
def login_page():
    return render_template("login.html")

# User Type Page Route
@app.route("/user-type")
@login_required
def user_type():
    return render_template("user_type.html")

# Chatbot Route
@app.route("/chat")
@login_required
def chat_page():
    return render_template("chat.html")


# Speech-to-Text API
@app.route('/speech-to-text', methods=['POST'])
@login_required
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
@login_required
def text_to_speech():
    text = request.json.get("text", "")
    tts = gTTS(text=text, lang="en")
    filename = "static/audio/output.mp3"
    tts.save(filename)
    return jsonify({"audio_url": f"/{filename}"})

# Emergency Alert API
@app.route('/emergency-alert', methods=['POST'])
@login_required
def emergency_alert():
    return jsonify({"message": "Emergency alert sent to contacts!"})

if __name__ == "__main__":
    if not os.path.exists("static/audio"):
        os.makedirs("static/audio")
    app.run(debug=True)