from dataclasses import dataclass

@dataclass
class EmotionLog:
    #Fields that takes in the id of the user, id of the log, the emotion label, a description of the situation, the perceived trigger of the emotion, the intensity of the emotion, the sleep quality of the user, and the date it occurred.
    user_id: int
    log_id: int
    label: str
    situation_description: str 
    log_date: str
    perceived_trigger: str
    intensity: int
    sleep_quality: str
    follow_up_qa: str

    def to_dict(self):
        # Takes no parameters. Turns the EmotionLog instance into a python dictionary.
        return {
            "log_id": self.log_id,
            "user_id": self.user_id,
            "label": self.label,
            "situation_description": self.situation_description,
            "log_date": self.log_date,
            "perceived_trigger": self.perceived_trigger,
            "intensity": self.intensity,
            "sleep_quality": self.sleep_quality,
            "follow_up_qa": self.follow_up_qa
        }
    
    def from_dict(d):
        # Takes no parameters. Turns the emotion log dictionary into an EmotionLog instance.
        return EmotionLog(d.user_id, d.log_id, d.label, d.situation_description, d.log_date, d.perceived_trigger, d.intensity, d.sleep_quality, d.follow_up_qa)


    def __str__(self):
        return f"{self.log_id} | {self.user_id} | {self.label} | {self.situation_description} | {self.log_date} | {self.perceived_trigger} | {self.intensity} | {self.sleep_quality} | {self.follow_up_qa} ||"
