from logger.logger import Logger

from langchain_core.messages import ToolMessage
from langchain_core.runnables import RunnableLambda
from langgraph.prebuilt.tool_node import ToolNode

def create_tool_node_with_fallback(tool_node: ToolNode) -> dict:
    try:
        return tool_node.with_fallbacks(
            [RunnableLambda(handle_tool_error)], exception_key="error"
        )
    except:
        Logger.error("Error to create_tool_node_with_fallback", __name__)

def handle_tool_error(state) -> dict:
    """
        Handle exceptions whenever a tool have an execution error.
    """
    try:
        error = state.get("error")
        tool_calls = state["messages"][-1].tool_calls
        return {
            "messages": [
                ToolMessage(
                    content=f"Error: {repr(error)}\n please fix your mistakes.",
                    tool_call_id=tc["id"],
                )
                for tc in tool_calls
            ]
        }
    except:
        Logger.error("Error to handle_tool_error with state: " + str(state), __name__)
