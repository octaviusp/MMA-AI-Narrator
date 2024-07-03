from logger.logger import Logger
from langchain_core.messages import ToolMessage

from typing import Optional

def delegate_function(state) -> dict:
    """
        Delegate to other and push on top of stack nan agent
    """
    messages = []
    tool_calls = state["messages"][-1].tool_calls
    agent_name = ""
    try:
        if tool_calls:
            # Note: Doesn't currently handle the edge case where the llm performs parallel tool calls
            agent_name = tool_calls[0]["args"]["agent_required"]
            messages.append(
                ToolMessage(
                    content=f"""The narrator_text is delegating runtime to {agent_name}""",
                    tool_call_id=tool_calls[0]["id"],
                    additional_kwargs={"agent_required": agent_name}
                )
            )
    except:
        Logger.error("Error to execute delegate function with state: " + str(state), __name__)

    return {
        "call_stack": agent_name,
        "messages": messages,
    }

def rollback_function(state) -> dict:
    """Pop the dialog stack and return to the main assistant.

    This lets the full graph explicitly track the dialog flow and delegate control
    to specific sub-graphs.
    """
    messages = []
    try:
        if state["messages"][-1].tool_calls:
            # Note: Doesn't currently handle the edge case where the llm performs parallel tool calls
            messages.append(
                ToolMessage(
                    content="""narrator_text agent is taking the control. Think what to do next, if you have enough information to answer the user query, do it. If not, think and reason what to do to meet user requirements.""",
                    tool_call_id=state["messages"][-1].tool_calls[0]["id"],
                )
            )
    except:
        Logger.error("Error to execute rollback function with state: " + str(state), __name__)

    return {
        "call_stack": "pop",
        "messages": messages,
    }

def update_call_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    try:
        if right is None:
            return left
        if right == "pop":
            return left[:-1]
        return left + [right]
    except:
        Logger.error("Error to update call_stack", __name__)
  
