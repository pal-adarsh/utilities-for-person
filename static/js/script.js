// Accessibility Settings
function changeFontSize() {
    const fontSize = document.getElementById("fontSize").value;
    document.body.style.fontSize = fontSize;
}

function changeContrast() {
    const contrast = document.getElementById("contrast").value;
    if (contrast === "high") {
        document.body.style.backgroundColor = "black";
        document.body.style.color = "white";
    } else {
        document.body.style.backgroundColor = "#f0f0f0";
        document.body.style.color = "#333";
    }
}

// Speech-to-Text
function convertSpeechToText() {
    let fileInput = document.getElementById("audioFile");
    let formData = new FormData();
    formData.append("audio", fileInput.files[0]);

    fetch("/speech-to-text", {
        method: "POST",
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("speechResult").innerText = data.text || data.error;
    });
}

// Text-to-Speech
function convertTextToSpeech() {
    let text = document.getElementById("textInput").value;

    fetch("/text-to-speech", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: text })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById("audioPlayer").src = data.audio_url;
    });
}

// Audio Note-Taking
let mediaRecorder;
let audioChunks = [];

function startRecording() {
    navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            mediaRecorder = new MediaRecorder(stream);
            mediaRecorder.ondataavailable = event => {
                audioChunks.push(event.data);
            };
            mediaRecorder.onstop = () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
                const audioURL = URL.createObjectURL(audioBlob);
                const audioElement = document.createElement('audio');
                audioElement.controls = true;
                audioElement.src = audioURL;
                document.getElementById('notesList').appendChild(audioElement);
                audioChunks = []; // Reset the audioChunks array
            };
            mediaRecorder.start();
        })
        .catch(error => {
            console.error("Error accessing the microphone", error);
        });
}

function stopRecording() {
    mediaRecorder.stop();
}

// Sign Language Interpreter
let videoElement = document.getElementById("webcam");
let signResultElement = document.getElementById("signResult");
let currentStream = null;

function startSignLanguageInterpreter() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                currentStream = stream;
                videoElement.srcObject = stream;
                videoElement.style.display = "block";
            })
            .catch(function(err) {
                console.error("Error accessing webcam: ", err);
            });
    } else {
        alert("Webcam not supported.");
    }
}

function stopSignLanguageInterpreter() {
    if (currentStream) {
        currentStream.getTracks().forEach(track => track.stop());
        videoElement.style.display = "none";
        signResultElement.innerText = "Sign language interpreter stopped.";
    }
}

// Emergency Alert
function sendEmergencyAlert() {
    fetch("/emergency-alert", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: "Emergency Alert Sent!" })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
    });
}