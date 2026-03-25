import controller
from controller import emotion_log # from controller folder, import EmotionLog class
from model import llm_client # from model folder, import llm_client

# Test variables
log = "TestLog"


def save_log():
    assert controller.save_log(log) == True

def update_log():
    assert controller.update_log(1, log) == True

def user_exists_():
    assert controller.user_exists("JohnSmith", "JohnSmith") == True
    assert controller.user_exists("JohnSmith", "Yabadoo") == False

def verify_password():
    assert controller.verify_password("AwesomeSauce", "AwesomeSauce") == True
    assert controller.verify_password("AwesomeSauce", "1234") == False

def create_user():
    assert controller.create_user("Jimmyboy12", "coolpass") == True

def generate_chat_text():
    assert controller.generate_chat_text("prompt", [log]) == "response"

def generate_patterns_summary():
    assert controller.generate_patterns_summary() == "response"

def generate_followup_questions():
    assert controller.generate_followup_questions() == "response"

def llm_connect():
    assert llm_client.llm_connect("llm_url") == True

def db_llm_connect():
    assert llm_client.db_llm_connect("db_url","llm_url") == True

def generate_text():
    assert llm_client.generate_text("prompt") == "response"