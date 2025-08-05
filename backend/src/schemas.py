from pydantic import BaseModel
from typing import Optional

class CallData(BaseModel):
    callId: str
    callDate: Optional[str] = None
    fileUrl: str
    agentId: str
    event_time: str

class UserIn(BaseModel):
    username: str
    password: str

class AutoParams(BaseModel):
    QuestionID: str
    ButtonAlias: str
    HubComputerName: str
    POS: str
    UserText: Optional[str] = ""