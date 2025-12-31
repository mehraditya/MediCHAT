import random 
import time

class ModelError(Exception):
    pass


def dummy_model_inference(text: str, language: str) -> str:
    time.sleep(random.uniform(0.1, 0.5))
    if random.random() < 0.1: 
            raise ModelError("Model inference failed")
    if language == "hindi":
            return "यह सुनकर लग रहा है कि आप दबाव महसूस कर रहे हैं। कृपया थोड़ा और बताएं।"
    if language == "hinglish":
            return "Lagta hai kaafi pressure chal raha hai. Thoda aur share karna chahoge?"
    return "It sounds like your're under some pressure. Want to share more?"

# def generate_reply(text: str, language: str) -> tuple[str,str]:
#     if language == "hindi":
#         return ("मैं समझ सकता हूँ कि आप कैसा महसूस कर रहे हैं। क्या आप इसके बारे में बात करना चाहेंगे?","rule-based"
#         )
#     if language =="hinglish":
#         return ("Samajh aa raha hai, aap thoda stressed lag rahe ho. Chaaho toh baat kar sakte hain.","rule-based"
#         )
#     return ("I understand that you're feeling this way. Would you like to talk more about it?","rule-based"
#     )

def generate_reply(text: str, language: str) -> tuple[str,str]:
    try:
        reply = dummy_model_inference(text, language)
        return reply, "dummy-ml"
    except ModelError:
        return ("I'm here to listen. Could you try explaining that a bit more?","fallback")