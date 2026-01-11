from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import re
from typing import List, Optional
from time import perf_counter
from model_service import generate_reply




app = FastAPI()

v1_router = APIRouter(prefix="/v1") 

message_log: List[dict] = []

class ResponseMeta_data(BaseModel):
    model: Optional[str] = None
    confidence: Optional[float] = None
    processing_time_ms: Optional[int] = None

class MessageRequest(BaseModel):
    message:str

class MessageResponse(BaseModel):
    reply:str
    language:str
    meta: Optional[ResponseMeta_data] = None

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

#language detection 
def detect_language(text: str) ->str:
    #Hindi
    if re.search(r'[\u0900-\u097F]', text):
        return "hindi"
    
    hinglish_keys = ["hai","nahi","kyun","kya","kaise","haan","problem","stress","tension"
    ]

    lowered = text.lower()
    for word in hinglish_keys:
        if word in lowered:
            return "hinglish"
    return "english"
    

def process_message(text: str) ->tuple[str, str, str]:  
    language = detect_language(text)
    reply, model_name = generate_reply(text, language)
    return reply, language, model_name   


@v1_router.post("/message", response_model = MessageResponse)
def send_message(payload: MessageRequest):
    #accept user response and return response
    start = perf_counter()
    #validating message
    validate_message(payload.message)


    reply, language, model_name = process_message(payload.message)

    #for response time
    elapsed_time = int((perf_counter() - start) *1000)

    #for memory 
    message_log.append({
        "user_message": payload.message,
        "reply": reply,
        "language": language,
        "model": model_name
    })

    return MessageResponse(
        reply = reply,
        language = language,
        meta = ResponseMeta_data(
            model = model_name,
            processing_time_ms = elapsed_time
        )
    )

@v1_router.get("/health")
def health_check():
    return {
        "status": "ok"
        "service: medichat-backend"
    }

@v1_router.get("/messages")
def get_messages():
    return {
        "count": len(message_log),
        "messages": message_log
    }

@v1_router.delete("/messages")
def delete_message():
    message_log.clear()
    return {
        "status": "cleared",
        "count": 0
    }

app.include_router(v1_router)