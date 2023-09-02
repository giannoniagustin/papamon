from dataclasses import dataclass,field
@dataclass
class Time:
    hour :int =field(default=0)
    minute : int = field(default=0) 
    second : int = field(default=0) 
    

    