from core.graph.utils.names import rollback

from langchain_core.callbacks import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from langchain_core.tools import BaseTool
from langchain_core.messages import AIMessage, ToolCall

from typing import  Optional, Union

class Rollback(BaseTool):
    """Used for subagents to return control back to the narrator_text"""

    name: str = rollback
    description: str = (
        "Whenever you finalize your task, ensure that you return control to the narrator_text. This means completing all necessary steps to gather and analyze the data, providing the user with the relevant information or video links, and then signaling to the narrator_text that the task is complete and control can be handed back for further processing or next steps. This tool doesn't require arguments."
    )

    def _run(
        self,
        run_manager: Optional[CallbackManagerForToolRun] = None,
        **args,
    ) -> Union[str, Exception]:
        """Execute the code synchronously."""
        try:
            """Pop the dialog stack and return to the main assistant.
            This lets the full graph explicitly track the dialog flow and delegate control
            to specific sub-graphs.
            """
            return AIMessage(tool_calls=[ToolCall(name=rollback)])
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
            return AIMessage(tool_calls=[ToolCall(name=rollback)])
        except Exception as e:
            return repr(e)
