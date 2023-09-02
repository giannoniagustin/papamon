from dataclasses import dataclass,field
from datetime import time

@dataclass
class Scheduler:
    monday :list[time] = field(default_factory=list)
    tuesday :list[time] = field(default_factory=list)
    wednesday :list[time] = field(default_factory=list)
    thursday :list[time] = field(default_factory=list)
    friday :list[time] = field(default_factory=list)
    saturday :list[time] = field(default_factory=list)
    sunday :list[time] = field(default_factory=list)

   


    