def generate_reply(intent: str, language: str) -> str:
    if language == "hindi":
        return _hindi(intent) 
    if language == "hinglish":
        return _hinglish(intent)
    return _en(intent)

def _en(intent):
    responses = {"neutral": "I’m here with you. What’s on your mind?",
        "venting": "It sounds like you’ve been holding a lot in. You can share more if you want.",
        "emotional": "I’m really sorry you’re feeling this way. Want to tell me what’s been weighing on you?",
        "crisis": "I’m really glad you reached out. You’re not alone, and help is available."}

def _hinglish(intent: str) -> str:
    responses = {}

def _hindi(intent: str) ->str:
    responses = {}