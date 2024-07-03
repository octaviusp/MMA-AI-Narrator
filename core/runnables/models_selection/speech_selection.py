from config.config import KEYS, config_instance
from openai import AsyncOpenAI

class SpeechRecognition:

    @classmethod
    def OpenAI_TTS(self, max_retries: int = 2, timeout: float = 15,**kwargs) -> AsyncOpenAI:
        return AsyncOpenAI(
            api_key=config_instance.get_env(KEYS.OPENAI_API_KEY),
            max_retries=max_retries,
            timeout=timeout,
            **kwargs
        )