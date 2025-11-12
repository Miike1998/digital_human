from flask import Flask, request, jsonify
from flask_cors import CORS
from speech_to_text import transcribe_audio
from text_to_speech import synthesize_speech
from chat_ai import generate_reply

app = Flask(__name__)
CORS(app)  # maakt frontend-requests mogelijk

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        audio = request.files.get("audio")
        if not audio:
            return jsonify({"error": "Geen audiobestand ontvangen"}), 400

        user_text = transcribe_audio(audio)
        ai_reply = generate_reply(user_text)
        audio_path = synthesize_speech(ai_reply)

        return jsonify({
            "user_text": user_text,
            "ai_reply": ai_reply,
            "audio_url": f"/static/{audio_path}"
        })

    except Exception as e:
        print("❌ Fout in /api/chat:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
