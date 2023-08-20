from dataclasses import dataclass
from model.Raspberry import Raspberry
from model.Status import Status
@dataclass
class StatusRaspberies:
    raspberry :Raspberry 
    status : Status
    

    