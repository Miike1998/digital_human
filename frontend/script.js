const recordButton = document.getElementById("recordButton");
const transcriptEl = document.getElementById("transcript");
const replyAudio = document.getElementById("replyAudio");

let mediaRecorder;
let audioChunks = [];

recordButton.addEventListener("click", async () => {
  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    startRecording();
  } else {
    stopRecording();
  }
});

async function startRecording() {
  recordButton.textContent = "🛑 Stop opname";
  const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
  mediaRecorder = new MediaRecorder(stream);
  audioChunks = [];

  mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
  mediaRecorder.onstop = sendAudioToBackend;
  mediaRecorder.start();
}

async function stopRecording() {
  recordButton.textContent = "🎤 Start gesprek";
  mediaRecorder.stop();
}

async function sendAudioToBackend() {
  const blob = new Blob(audioChunks, { type: "audio/wav" });
  const formData = new FormData();
  formData.append("audio", blob, "user_audio.wav");

  transcriptEl.textContent = "⏳ Even luisteren...";
  const response = await fetch("http://127.0.0.1:5000/api/chat", {
    method: "POST",
    body: formData,
  });

  const data = await response.json();
  transcriptEl.textContent = `👤 Jij: ${data.user_text}\n🤖 AI: ${data.ai_reply}`;
  replyAudio.src = data.audio_url;
  replyAudio.play();
}
