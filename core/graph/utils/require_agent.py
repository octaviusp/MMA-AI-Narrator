from logger.logger import Logger

from langchain_core.messages import ToolCall

from typing import List

def require_agent(tool_calls: List[ToolCall], agent_name: str):
    try:
        agent_required = tool_calls[0]["args"]["agent_required"]
        if agent_name == "" and agent_required:
            return "delegate"
        return agent_required == agent_name
    except Exception as e:
        Logger.error(f"Error checking required agent in tool calls: {e}", __name__)
        return False  # Assuming default return or handling could be discussed