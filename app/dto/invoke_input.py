from pydantic import BaseModel

class InvokeInputDTO(BaseModel):
    session_id: str
    query: str