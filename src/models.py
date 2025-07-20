import datetime as dt
from pydantic import BaseModel, Field

class ActivityType(BaseModel):
     type_id: int = Field(alias="typeId")
     type_key: str = Field(alias="typeKey")

class GarminActivity(BaseModel):
    activity_id: int = Field(alias="activityId")
    start_time: dt.datetime = Field(alias="startTimeLocal")
    duration: float
    distance: float
    activity_type: ActivityType = Field(alias="activityType")
    activity_name: str = Field(alias="activityName", default = None) # sometimes the field is missing in the response
    
    class Config:
        validate_by_name = True

    @property
    def distance_km(self) -> float:
        return self.distance/1000.0

    @property
    def duration_min(self) -> float:
        return self.duration/60.0

    @property
    def date(self) -> dt.date:
        return self.start_time.date()

    @property
    def place(self) -> str:
        places = {'berlin', 'cisternino', 'sarstedt', 'wittenberg', 'toulouse'}
        words = self.activity_name.lower().replace(',','').split() # simple tokenization
        match = list(set(words) & places)
        return match[0].capitalize() if match else ''

    def export(self) -> dict:
        return {'id': self.activity_id,
                'place': self.place,
                'date': self.date,
                'distance_km': self.distance_km,
                'duration_min': self.duration_min}