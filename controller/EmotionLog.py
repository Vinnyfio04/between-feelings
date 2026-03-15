from dataclasses import dataclass

@dataclass
class EmotionLog:
    #Fields that takes in the id of the user, id of the log, the emotion label, a description of the situation, the perceived trigger of the emotion, the intensity of the emotion, the sleep quality of the user, and the date it occurred.
    user_id: int
    log_id: int
    label: str
    situation_description: str
    perceived_trigger: str
    intensity: int
    sleep_quality: str
    log_date: str

    def to_dict():
        # Takes no parameters. Turns the EmotionLog instance into a python dictionary.
        return {}
    
    def from_dict():
        # Takes no parameters. Turns the emotion log dictionary into an EmotionLog instance.
        return EmotionLog(1, 1, "label", "description", "trigger", "intesity", "sleep quality", "1000-1-31")






