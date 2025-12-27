from fastapi import FastAPI 
from pydantic import BaseModel

app = FastAPI()

class MessageRequest(BaseModel):
    message:str

class MessageResponse(BaseModel):
    reply:str
    language:str

@app.post("/message", response_model = MessageResponse)
def send_message(payload: MessageRequest):
    #accept user response and return response
    return MessageResponse(
        reply = "Received messaage",
        language = "unknown"
    )