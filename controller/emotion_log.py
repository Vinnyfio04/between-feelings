from dataclasses import dataclass
from typing import Any, Dict

@dataclass
class EmotionLog:
    #Fields that takes in the id of the user, id of the log, the emotion label, a description of the situation, the perceived trigger of the emotion, the intensity of the emotion, the sleep quality of the user, and the date it occurred.
    user_id: int
    log_id: int
    label: str
    description: str
    date: str
    trigger: str
    intensity: int
    sleep_quality: str
    follow_up_qa: str

    def to_dict(self) -> Dict[str, Any]:
        # Convert this EmotionLog instance into a dictionary.
        return {
            "log_id": self.log_id,
            "user_id": self.user_id,
            "label": self.label,
            "description": self.description,
            "date": self.date,
            "trigger": self.trigger,
            "intensity": self.intensity,
            "sleep_quality": self.sleep_quality,
            "follow_up_qa": self.follow_up_qa
        }
    
    @staticmethod
    def from_dict(d: Dict[str, Any]) -> "EmotionLog":
        # Build an EmotionLog from a dictionary.
        return EmotionLog(
            user_id=d["user_id"],
            log_id=d["log_id"],
            label=d["label"],
            description=d["description"],
            date=d["date"],
            trigger=d["trigger"],
            intensity=d["intensity"],
            sleep_quality=d["sleep_quality"],
            follow_up_qa=d["follow_up_qa"],
        )


    def to_prompt_row(self) -> str:
        """Serialize this log into the standardized prompt row format."""
        return f"{self.log_id} | {self.user_id} | {self.label} | {self.description} | {self.date} | {self.trigger} | {self.intensity} | {self.sleep_quality} | {self.follow_up_qa} ||"

    def __str__(self):
        return self.to_prompt_row()
