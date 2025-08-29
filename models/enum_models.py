from enum import Enum

class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

class Goal(Enum):
    LOSS_WEIGHT = "loss_weight"
    GAIN_MUSCLE = "gain_muscle"
    MAINTAIN = "maintain"

class Experience(Enum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"