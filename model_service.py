import os
import random
import time
from transformers import pipeline
from safety_service import is_safe, safe_fallback

class ModelError(Exception):
    pass



def _rule_based_model(text: str, language:str) ->str:
    if language =="hindi":return "मैं समझ सकता हूँ कि आप कैसा महसूस कर रहे हैं। क्या आप इसके बारे में बात करना चाहेंगे?"

    if language =="hinglish":return "Samajh aa raha hai, aap thoda stressed lag rahe ho. Chaaho toh baat kar sakte hain."

    return "I understand that you're feeling this way. Would you like to talk more about it?"



def _dummy_ml_model(text: str, language:str) ->str:
    time.sleep(random.uniform(0.1,0.5))
    if random.random() <0.1:raise ModelError("Dummy model failed")
    if language =="hindi":
        return "यह सुनकर लग रहा है कि आप दबाव महसूस कर रहे हैं। कृपया थोड़ा और बताएं।"

    if language =="hinglish":
        return "Lagta hai kaafi pressure chal raha hai. Thoda aur share karna chahoge?"

    return "It sounds like you’re under some pressure. Want to share more?"

_text_generator = None
def _load_real_model():
    global _text_generator 
    if _text_generator is None:
        _text_generator = pipeline("text-generation", model="distilgpt2")

def _real_model(text: str, language: str) ->str:
    _load_real_model()

    prompt = ("Respond to message:\n"
              f"{text}\nResponse:")
    
    result = _text_generator(
        prompt,
        max_length = 100,
        do_sample = True,
        temperature = 0.6
    )
    return result[0]["generated_text"].split("Response:")[-1].strip()

def generate_reply(text: str, language:str) ->tuple[str,str]:
    """
    Routes to the active model based on configuration.
    """

    active_model = os.getenv("MEDCHAT_MODEL","dummy")
    try:
        if active_model =="rule":
            reply = _rule_based_model(text, language)
            model_name ="rule-based"

        elif active_model =="dummy":
            reply = _dummy_ml_model(text, language)
            model_name ="dummy-ml"

        elif active_model =="real":
            reply = _real_model(text, language)
            model_name ="real-ml"

        else:
            reply = _rule_based_model(text, language)
            model_name ="fallback"

    except ModelError:return safe_fallback(language),"fallback"

    if not is_safe(reply):
        return safe_fallback(language), "safety-fallback"
    
    return reply, model_name