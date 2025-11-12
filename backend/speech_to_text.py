import azure.cognitiveservices.speech as speechsdk
import os
from tempfile import NamedTemporaryFile
from pydub import AudioSegment
import dotenv
dotenv.load_dotenv()

speech_key = os.environ.get("AZURE_KEY")
region = os.environ.get("AZURE_REGION")

def transcribe_audio(audio_file):
    """Zet elke opname om naar PCM WAV (16kHz mono) en transcribeer met Azure."""
    # 1️⃣ Sla tijdelijk de originele upload op (meestal WebM of MPEG)
    with NamedTemporaryFile(delete=False, suffix=".webm") as temp_in:
        audio_file.save(temp_in.name)

    # 2️⃣ Converteer naar geldig WAV-formaat
    with NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
        try:
            sound = AudioSegment.from_file(temp_in.name)
        except Exception as e:
            raise RuntimeError(f"Kan opname niet openen: {e}")
        sound = sound.set_frame_rate(16000).set_channels(1).set_sample_width(2)
        sound.export(temp_wav.name, format="wav")

    # 3️⃣ Controleer of WAV leesbaar is
    if os.path.getsize(temp_wav.name) < 1000:
        raise RuntimeError("WAV-bestand lijkt leeg of ongeldig.")

    # 4️⃣ Azure STT
    try:
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
        audio_config = speechsdk.AudioConfig(filename=temp_wav.name)
        recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
        result = recognizer.recognize_once()
    except Exception as e:
        raise RuntimeError(f"Azure STT fout: {e}")

    if not result.text:
        raise RuntimeError("Geen spraak herkend.")

    return result.text
