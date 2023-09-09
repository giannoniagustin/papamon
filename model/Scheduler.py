from dataclasses import dataclass,field
from datetime import time
from model.Time import Time

@dataclass
class Scheduler:
    monday :list[Time] = field(default_factory=list)
    tuesday :list[Time] = field(default_factory=list)
    wednesday :list[Time] = field(default_factory=list)
    thursday :list[Time] = field(default_factory=list)
    friday :list[Time] = field(default_factory=list)
    saturday :list[Time] = field(default_factory=list)
    sunday :list[Time] = field(default_factory=list)

   


    