from core.graph.functions.call_stack import update_call_stack

from langgraph.graph.message import AnyMessage, add_messages
from langchain_core.messages import BaseMessage

from typing import Annotated, Literal, TypedDict

agents = Literal["narrator_text",  "narrator_vision"]
    
class State(TypedDict):
    # Messages son la lista de messages, todos heredan BaseMessage
    # e.g: IAMessage, HumanMessage... 
    frames_b64: list[str] = []
    history: list[BaseMessage] = []
    messages: Annotated[list[AnyMessage], add_messages]
    # extra_info es alguna info adicional que se tenga que pasar por el estado
    # user_ids, informacion extra del que llama etc... 
    extra_info: str
    # call_stack: la pila de llamadas/ejecuciones
    # en literal tenes que agregar TODOS los agentes
    # la funcion del final es la funcion de pop o push en una pila.
    call_stack: Annotated[
        list[agents],
        update_call_stack,
    ]