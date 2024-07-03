
from core.runnables.models_selection.llm_selection import LLM
from config.config import KEYS, config_instance

from langchain_core.messages import HumanMessage

API_KEY = config_instance.get_env(KEYS.OPENAI_API_KEY)

# TO DO: AGREGARLO COMO PIPELINE EN  EL GRAFO PARA QUE RSUMA LOS MESSAGES!
async def resume_text(large_text: str):
    """
        Call this for ask gpt-3.5-turbo/gpt-4-turbo to resume the data.
    """
    task = f"""Please,
            maintaining the key points, titles, definitions, and important topics/questions.
            Resume the following text: \n{large_text}. \n
            Go directly to the point, extract key details as i already mention. Make it shortly and fast."""
    
    return (await LLM.chat_gpt_3_5_turbo(api_key=API_KEY).ainvoke([HumanMessage(content=task)])).content
