import io
import time
from google.cloud import texttospeech
import soundfile as sf
import sounddevice as sd
import numpy as np

class TextToSpeechPlayer:
    def __init__(self):
        # Instantiates a client
        self.client = texttospeech.TextToSpeechClient()

    def synthesize_speech(self, text, language_code="en-US", gender=texttospeech.SsmlVoiceGender.MALE):
        # Set the text input to be synthesized
        synthesis_input = texttospeech.SynthesisInput(text=text)

        # Build the voice request, select the language code and the ssml voice gender
        voice = texttospeech.VoiceSelectionParams(
            language_code=language_code, ssml_gender=gender
        )

        # Select the type of audio file you want returned
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

        # Perform the text-to-speech request on the text input with the selected voice parameters and audio file type
        response = self.client.synthesize_speech(
            input=synthesis_input, voice=voice, audio_config=audio_config
        )

        return response.audio_content

    def generate_voice(self, voice_bytes):
        # Read the audio bytes from the response
        audio_bytes = b''.join(voice_bytes)
        
        # Use an in-memory buffer to convert bytes to an audio stream
        buffer = io.BytesIO(audio_bytes)
        data, samplerate = sf.read(buffer)
        
        # Ensure the audio data is in the correct format for playback
        audio_stream = np.array(data, dtype=np.float32)
        
        return audio_stream, samplerate

    def play_audio_stream(self, audio_stream, samplerate):
        sd.play(audio_stream, samplerate=samplerate)
        sd.wait()

if __name__ == "__main__":
    tts_player = TextToSpeechPlayer()
    text = "Hello, World!"

    # Synthesize speech
    start = time.time()
    audio_content = tts_player.synthesize_speech(text)

    # Generate voice stream
    audio_stream, samplerate = tts_player.generate_voice([audio_content])

    # Play audio stream
    tts_player.play_audio_stream(audio_stream, samplerate)
    print(time.time() - start)