from core.runnables.agents.agent_factory import AgentFactory  
from core.runnables.models_selection.llm_selection import LLM
from core.graph.utils.names import narrator_text

# Configuration for the LLM and API key
llm = LLM.groq_llama_3_70b(temperature=1, max_retries=2, timeout=15)

system_prompt = f"""
You are an AI MMA Fight Narrator. Comment on received fight situations dramatically with brief and short words.
Your response must be no greater than 6 words. Answer directly the dramatic commentary.
Examples:
    Scene: the image shows a fighter throw a kick to the head of the other.
    You: Ouuu! what a kick!!!

    Scene: the image shows a fighter doing a takedown to the other.
    You: Great takedown!
"""

# Use the AgentFactory to create the narrator_text runnable
runnable = AgentFactory.create(agent_name=narrator_text,
                                tools=[], 
                                system_prompt=system_prompt,
                                conversation_history=False,
                                llm=llm)