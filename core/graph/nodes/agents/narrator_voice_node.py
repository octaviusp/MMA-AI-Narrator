from core.runnables.executor.runnable_executor import OpenAISpeechRecognitionModel
from core.runnables.models_selection.speech_selection import SpeechRecognition
from core.graph.utils.names import narrator_voice


client = SpeechRecognition.OpenAI_TTS()

runnable = OpenAISpeechRecognitionModel(name=narrator_voice, client=client, speed=1.1)