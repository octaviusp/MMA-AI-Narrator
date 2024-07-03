from config.config import Config, config_instance

from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_nvidia_ai_endpoints import ChatNVIDIA

class LLM:

    """
    STATIC CLASS LLM for instance management of language learning models (LLMs).
    This class provides static methods to instantiate various LLMs with specified configurations.

    Methods:
        chat_gpt_custom(model: str, temperature: int, **kwargs) - Instantiates a custom ChatOpenAI model with specified settings.
        chat_gpt_3_5_turbo(temperature: int, **kwargs) - Instantiates a ChatOpenAI model with the "gpt-3.5-turbo" configuration.
        groq_custom(model: str, max_retries: int, temperature: int, **kwargs) - Instantiates a custom ChatGroq model with specified settings.
        groq_mixtral_7x8b(max_retries: int, temperature: int, **kwargs) - Instantiates a ChatGroq model with the "mixtral-8x7b-32768" configuration.
        groq_llama_3_70b(max_retries: int, temperature: int, **kwargs) - Instantiates a ChatGroq model with the "llama3-70b-8192" configuration.
        groq_llama_3_8b(max_retries: int, temperature: int, **kwargs) - Instantiates a ChatGroq model with the "llama3-8b-8192" configuration.
    """

    def __init__(self, config: Config):
        self.config = config

    @staticmethod
    def chat_nvidia(
        model: str = "",
        temperature: int = 0.1, **kwargs) -> ChatNVIDIA:

        return ChatNVIDIA(
            model=model,
            temperature=temperature,
            **kwargs
        )

    @staticmethod
    def chat_gpt_custom(
        model: str,
        temperature: int = 0.1, **kwargs) -> ChatOpenAI:
        return ChatOpenAI(
            base_url = "https://integrate.api.nvidia.com/v1",
            api_key = config_instance.get_env(Config.KEYS.NVIDIA_API_KEY),
            model=model,
            temperature=temperature,
            **kwargs
        )

    @staticmethod
    def chat_gpt_4o(
        temperature: int = 0.1, **kwargs) -> ChatOpenAI:

        return ChatOpenAI(
            model="gpt-4o",
            temperature=temperature,
            **kwargs
        )

    # DEPRECATED
    """    @staticmethod
        def chat_gpt_4_turbo(
            temperature: int = 0.1, **kwargs) -> ChatOpenAI:

            return ChatOpenAI(
                model="gpt-4-turbo",
                temperature=temperature,
                **kwargs
            )"""

    @staticmethod
    def chat_gpt_3_5_turbo(
        temperature: int = 0.1, **kwargs) -> ChatOpenAI:

        return ChatOpenAI(
            model="gpt-3.5-turbo",
            temperature=temperature,
            **kwargs
        )

    @staticmethod
    def gemini_1_5_flash_001(
        temperature: int = 0.1, **kwargs) -> ChatGoogleGenerativeAI:

        return ChatGoogleGenerativeAI(
            model="gemini-1.5-flash-001",
            temperature=temperature,
            **kwargs
        )

    @staticmethod
    def gemini_1_0_pro_002(
        temperature: int = 0.1, **kwargs) -> ChatGoogleGenerativeAI:

        return ChatGoogleGenerativeAI(
            model="gemini-pro",
            temperature=temperature,
            **kwargs
        )

    @staticmethod
    def groq_custom(model: str,
                    max_retries: int,
                    temperature: int = 0.1,
                    **kwargs
                    ) -> ChatGroq :
        
        return ChatGroq(
            model=model,
            max_retries=max_retries,
            temperature=temperature,
            **kwargs
        )
    
    @staticmethod
    def groq_mixtral_7x8b(
                    max_retries: int,
                    temperature: int = 0.1,
                    **kwargs
                    ) -> ChatGroq :
        
        return ChatGroq(
            model='mixtral-8x7b-32768',
            max_retries=max_retries,
            temperature=temperature,
            **kwargs
        )

    @staticmethod
    def groq_llama_3_70b(
                    max_retries: int,
                    temperature: int = 0.1,
                    **kwargs
                    ) -> ChatGroq :
        
        return ChatGroq(
            model="llama3-70b-8192",
            max_retries=max_retries,
            temperature=temperature,
            **kwargs
        )

    @staticmethod
    def groq_llama_3_8b(
                    max_retries: int,
                    temperature: int = 0.1,
                    **kwargs
                    ) -> ChatGroq :
        
        return ChatGroq(
            model="llama3-8b-8192",
            max_retries=max_retries,
            temperature=temperature,
            **kwargs
        )
    