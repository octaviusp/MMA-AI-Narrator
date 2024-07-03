from config.config import KEYS, config_instance
from openai import AsyncOpenAI
from enum import Enum

class VisionRecognition:

    class Model(Enum):
        microsoft_phi_3 = "microsoft/phi-3-vision-128k-instruct"
        adept_fuyu_8b = "adept/fuyu-8b"
        nvidia_neva_22b= "nvidia/neva-22b"

    @classmethod
    def OpenAI_Vision(self, max_retries: int = 2, timeout: float = 15, **kwargs) -> AsyncOpenAI:
        return AsyncOpenAI(
            api_key=config_instance.get_env(KEYS.OPENAI_API_KEY),
            max_retries=max_retries,
            timeout=timeout,
            **kwargs
        )