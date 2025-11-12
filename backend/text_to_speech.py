import azure.cognitiveservices.speech as speechsdk
import os
from datetime import datetime
import dotenv
dotenv.load_dotenv()

speech_key = os.environ.get("AZURE_KEY")
region = os.environ.get("AZURE_REGION")

def synthesize_speech(text):
    """Genereer een mp3-bestand van AI-antwoord"""
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=region)
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    file_name = f"reply_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
    file_path = f"../frontend/static/{file_name}"
    audio_config = speechsdk.audio.AudioOutputConfig(filename=file_path)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    synthesizer.speak_text_async(text).get()
    return file_name
