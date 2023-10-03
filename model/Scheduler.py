from dataclasses import dataclass,field
from model.Time import Time
from typing import List

@dataclass
class Scheduler:
    monday :List[Time] = field(default_factory=list)
    tuesday :List[Time] = field(default_factory=list)
    wednesday :List[Time] = field(default_factory=list)
    thursday :List[Time] = field(default_factory=list)
    friday :List[Time] = field(default_factory=list)
    saturday :List[Time] = field(default_factory=list)
    sunday :List[Time] = field(default_factory=list)

   


    