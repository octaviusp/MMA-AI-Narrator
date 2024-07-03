from typing import Optional
from pydantic import BaseModel

class InvokeRequest(BaseModel):
    config: Optional[dict] = None
    session_id: str
    content: str

###############################
# THIS ARE THE PROTOCOLS OF COMMUNICATION ACROSS AGENTS
##############################
