from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class MessageRequest(BaseModel):
    message:str

class MessageResponse(BaseModel):
    reply:str
    language:str

def validate_message(text: str) -> None:
    cleaned = text.strip() 
    if not cleaned:raise HTTPException(
        status_code = 400,
        detail = "Message cannot be empty"
    )
    if len(cleaned) <5:raise HTTPException(
        status_code = 400,
        detail = "Message is too short"
    )

@app.post("/message", response_model = MessageResponse)
def send_message(payload: MessageRequest):
    #accept user response and return response
    #validating message
    validate_message(payload.message)
    return MessageResponse(
        reply = "Received messaage",
        language = "unknown"
    )