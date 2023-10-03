from dataclasses import dataclass,field
from model.Raspberry import Raspberry
from model.StatusSlave import StatusSlave
from typing import List
@dataclass
class StatusSystem:
    slaves :List[Raspberry] = field(default_factory=list)
    slaveStatus: List[StatusSlave]= field(default_factory=list)
    status : bool= field(default_factory=False)
    message : str= field(default_factory="Not info")

    