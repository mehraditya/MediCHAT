from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import re


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
    
#response generation
def generate_reply(text: str, language: str) ->str:
    if language == "hi":
        return "मैं समझ सकता हूँ कि आप कैसा महसूस कर रहे हैं। क्या आप इसके बारे में बात करना चाहेंगे?"

    if language == "hinglish":
        return "Samajh aa raha hai, aap thoda stressed lag rahe ho. Chaaho toh baat kar sakte hain."

    # default
    return "I understand that you're feeling this way. Would you like to talk more about it?"

def process_message(text: str) ->tuple[str, str]:  
    language = detect_language(text)
    reply = generate_reply(text, language)
    return reply, language   


@app.post("/message", response_model = MessageResponse)
def send_message(payload: MessageRequest):
    #accept user response and return response
    #validating message
    validate_message(payload.message)
    reply, language = process_message(payload.message)
    return MessageResponse(
        reply = reply,
        language = language
    )