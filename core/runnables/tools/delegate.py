from pydantic import BaseModel, Field
from core.graph.utils.names import delegate, narrator_text_possible_agent_calls

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.messages import AIMessage, ToolCall

from typing import  Optional, Union

class DelegateInput(BaseModel):
    agent_required: str = Field(description=F"Agent name to move on. Availables: [{narrator_text_possible_agent_calls}]")

class Delegate(BaseTool):
    """Used for narrator_text for delegate to other agent"""

    name: str = delegate
    description: str = (
        "Whenever you need assistance from another agent, initiate a call to that agent. This involves identifying the specific capabilities or information required that are beyond your scope, selecting the appropriate agent to handle the task, and formally requesting their assistance. Ensure that you clearly communicate the nature of the task and any relevant context so that the agent can effectively complete their part. Once the agent has provided the necessary assistance, incorporate their input as needed and proceed with your task."
    )
    args_schema: type[BaseModel] = DelegateInput

    def _run(
        self,
        agent_required: str,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **args
    ) -> Union[str, Exception]:
        """Execute the code synchronously."""
        try:
            """Pop the dialog stack and return to the main assistant.
            This lets the full graph explicitly track the dialog flow and delegate control
            to specific sub-graphs.
            """
            return AIMessage(tool_calls=[ToolCall(name=delegate)])
        except Exception as e:
            return repr(e)

    async def _arun(
        self,
        code: str,
        run_manager: Optional[AsyncCallbackManagerForToolRun] = None,
        **args
    ) -> Union[str, Exception]:
        """Execute the code asynchronously."""
        try:
            return AIMessage(tool_calls=[ToolCall(name=delegate)])
        except Exception as e:
            return repr(e)
