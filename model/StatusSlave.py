from dataclasses import dataclass
from model.Raspberry import Raspberry
from model.Status import Status
@dataclass
class StatusSlave:
    
    raspberry :Raspberry 
    status : Status
    
    