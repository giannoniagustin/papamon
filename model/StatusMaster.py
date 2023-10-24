from dataclasses import dataclass,field
@dataclass
class StatusMaster:
    state :bool =field(default=None)
    lastReconstruct : str = field(default=None) 
    

    