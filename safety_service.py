import re

UNSAFE_WORDS = ["kill myself","suicide","die","murder","drug dealer","marijuana dealer","criminal","sociopath","hallucinating"]

def is_repetitive(text: str)->bool:
    text = text.lower()
    chunks = [text[i:i+50] for i in range(0,len(text), 50)]
    return len(chunks) >= 3 and len(set(chunks)) < len(chunks)

def contains_unsafe_words(text: str)->bool:
    lowered = text.lower()
    return any(keyword in lowered for keyword in UNSAFE_WORDS)

def is_safe(text: str)->bool:
    if len(text) > 500: 
        return False
    if contains_unsafe_words(text):
        return False
    if is_repetitive(text):
        return False
    return True



def safe_fallback(language: str) ->str:
    if language =="hindi":
        return "मुझे लगता है कि यह विषय थोड़ा संवेदनशील है। आप चाहें तो धीरे-धीरे अपनी बात साझा कर सकते हैं।"

    if language =="hinglish":
        return "Lagta hai yeh topic thoda sensitive ho sakta hai. Agar comfortable ho toh araam se share karo."

    return "I’m here to listen. If you’re comfortable, you can tell me a bit more about what’s going on."
