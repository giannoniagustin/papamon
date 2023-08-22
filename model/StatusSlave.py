from dataclasses import dataclass,field
from model.Raspberry import Raspberry
from model.Status import Status
@dataclass
class StatusSlave:
    state:bool = field(default=False)
    message: str  = field(default="Not connection")
    raspberry :Raspberry  = field(default=None)
    status : Status= field(default=None)
    
    