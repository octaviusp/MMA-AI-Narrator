from typing import Union
from core.models.messages import (
    AIMessage,
    NarratorSpeechMessage,
    FightVisionMessage,
)

from langchain_core.messages import BaseMessage

MessageType = Union[AIMessage,
                    NarratorSpeechMessage,
                    FightVisionMessage]

def turn_to(from_: BaseMessage, to_: MessageType) -> MessageType:
    """
        Convert a message from one type to another, for better graph track.
    """
    return to_(**from_.dict())