from core.graph.state.state_definition import State
from core.graph.utils.names import (
    rollback,
    tool_node
)
from logger.logger import Logger
from core.graph.utils.require_agent import require_agent

from langgraph.graph import END
from langgraph.prebuilt import tools_condition

from typing import Literal

# Tools
tool_or_end = Literal["tools", "__end__"]

def router_tools_or_rollback(state: State) -> Literal["tools", "rollback"]:
    try:
        tool_calls = state["messages"][-1].additional_kwargs.get("tool_calls", [])
        did_cancel = any(tc["function"]["name"] == rollback for tc in tool_calls)
        if did_cancel:
            return rollback
        return tool_node
    except Exception as e:
        Logger.error(f"Error in router_tools_or_rollback: {e}", __name__)
        return rollback  # Defaulting to rollback in case of error might not be ideal; needs specific handling strategy

possibles_ways = Literal[
    "__end__",
    "delegate"
]

possibles_agents = Literal[
    "narrator_vision"
]

def router_go_to_last_call_stack(state: State) -> possibles_agents:
    """
        Router to execute tool and back to the propietary agent executor
    """
    agent_name = state["call_stack"][-1]
    return agent_name

def router_select_agent(state: State) -> possibles_agents:
    """
        Router to select which agent the langgraph runtime will switch.
    """
    agent_name = state["messages"][-1].additional_kwargs["agent_required"]
    return agent_name

def router_narrator_text_end_or_delegate(state: State) -> possibles_ways:
    """
        This function determines the logic for the narrator_text to delegate to a sub-agent.
        It checks if the last message in the state has a ToolMessage.
        If it's a ToolMessage other than END, it takes its tool_calls which is a list of the first tool to call.
        This tool has a 'name' which is the parameter to call, in this parameter is the agent to be called, which is completed by reasoning.
        Thus, the narrator_text says based on the input, I need to call...
        and it calls.

        Normally you would add all the ifs with the possible agents that would be there.
        Normally if you have N agents, the number of ifs should be equal to N too.
        N edges pointing to the N agents.

        If none are met it means it is an END.
    """
    try:
        route = tools_condition(state)
        if route == END:
            return END
        
        tool_calls = state["messages"][-1].tool_calls
        if tool_calls:
            if require_agent(tool_calls, ""):
                return "delegate"
            return END
        # If no valid route
        raise ValueError("Invalid route")
    except Exception as e:
        Logger.error(f"Error in route_narrator_text: {e}", __name__)
        return END  # Defaulting to END on error could be revised based on desired error handling logic
