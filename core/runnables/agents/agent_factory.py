from core.prompts.prompt_factory import PromptFactory

from langchain_core.runnables import RunnableSerializable
from langchain_core.language_models import BaseChatModel
from langchain.tools import Tool

from typing import List, Type

class AgentFactory:
    """
    Factory class to create different types of agents with specified tools and prompts.
    """
    @staticmethod

    def create(agent_name: str,
                tools: List[Type[Tool]],
                system_prompt: str,
                llm: BaseChatModel,
                conversation_history: bool = False) -> RunnableSerializable:

        """
        Creates an agent with a specific configuration.

        :param agent_name: Name of the agent, used for identifying the type of agent being created.
        :param tools: List of tools to bind with the agent.
        :param prompt: Prompt configuration for the agent.
        :param llm: Language model inference system.
        :return: A runnable agent with the specified tools and prompt bound to the language model.
        """

        
        prompt = PromptFactory.create(
            system_prompt=system_prompt,
            conversation_history=conversation_history
        )

        #if len(tools):
        runnable =  prompt | llm #.bind_tools(tools)
        #else:
        #    runnable = prompt | llm
        runnable.name = agent_name
        
        return runnable