from logger.logger import Logger

from enum import Enum
from dotenv import load_dotenv
import os

class KEYS(Enum):
    API_KEY = "API_KEY"
    DATABASE_URL = "DATABASE_URL"
    SECRET_KEY = "SECRET_KEY"
    OPENAI_API_KEY="OPENAI_API_KEY"
    TAVILY_API_KEY="TAVILY_API_KEY"
    GOOGLE_API_KEY="GOOGLE_API_KEY"
    YOUTUBE_API_KEY="YOUTUBE_API_KEY"
    NVIDIA_API_KEY="NVIDIA_API_KEY"

Logger.info("Setting up config... ", __name__)
class Config:
    """
    Base class for configuration management using python-dotenv.
    This class handles loading environment variables and provides access to them through Enum keys.
    
    Attributes:
        KEYS (Enum): Enum class to hold environment variable keys, ensuring that they are accessed in a controlled manner.
        
    Methods:
        get_env(var: KEYS): Retrieves the value of the environment variable associated with the given Enum key.
    """
    
    def __init__(self):
        # In local development could be set into override==True
        load_dotenv(override=True)

    def get_env(self, key: KEYS):
        """
        Retrieves the value of the environment variable associated with the given Enum key.
        
        Args:
            var (Config.KEYS): The Enum key corresponding to the desired environment variable.
        
        Returns:
            str: The value of the environment variable.
        """
        return os.environ.get(key.value)

# Usage example:
# api_key = Config.get_env(Config.KEYS.API_KEY)
config_instance = Config()
Logger.info("Config loaded... ", __name__)