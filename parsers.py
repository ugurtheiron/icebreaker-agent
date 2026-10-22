from typing import Optional, Union

from pydantic import BaseModel, Field, model_validator

# Define the allowed categories
ALLOWED_CATEGORIES = [
    "Hunting",
    "Athletics",
    "Aikido",
    "Badminton",
    "Ballet",
    "Fishery",
    "Basketball",
    "Billiards",
    "Riding",
    "Bicycle",
    "Boxing",
    "Bushcraft",
    "Baseball",
    "Ice Hockey",
    "Ice Skating",
    "Bowling",
    "Dive",
    "Fitness",
    "Football",
    "Futsal",
    "Golf",
    "Wrestling",
    "Handball",
    "Hiking, Trekking, Outdoor",
    "Gymnastics and Trampoline",
    "Judo",
    "Camp",
    "Canoe and SUP",
    "Skiing, Snowboarding",
    "Running and Walking",
    "Karate",
    "Cricket",
    "Spade",
    "E-Sports",
    "Ping Pong",
    "Motorcycle",
    "Archery and Target Sports",
    "Orienteering",
    "Padel",
    "Skate, Skateboard, and Scooter",
    "Pickleball",
    "Pilates, Light Fitness Training",
    "Beach Tennis, Speedball",
    "Wind Sports",
    "Surfing",
    "Sporty Child and Physical Education",
    "Squash",
    "Tennis",
    "Climbing and Mountaineering",
    "Volleyball",
    "Windsurfing",
    "Sail",
    "Yoga",
    "Swimming",
]

# Category model with validation
class Category(BaseModel):
    predicted_category: str = Field(description="Predicted category")
    prediction_possibility: Optional[float] = Field(description="Predicted category possibility between 0 and 1")

    @model_validator(mode="before")
    @classmethod
    def validate_category(cls, values):
        category = values.get("predicted_category")
        if category not in ALLOWED_CATEGORIES:
            raise ValueError(f"Invalid category: {category}. Allowed categories are: {ALLOWED_CATEGORIES}")
        return values


class CategoryNotFound(BaseModel):
    warning: str = Field(description="Product category not found.")


class FinalResponse(BaseModel):
    final_output: Union[Category, CategoryNotFound]
