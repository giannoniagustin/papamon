from dataclasses import dataclass,field
from model.StatusMaster import StatusMaster
from model.StatusSlave import StatusSlave
from typing import List
@dataclass
class SystemStatus:
    slaveStatus: List[StatusSlave]= field(default_factory=list)
    masterStatus:StatusMaster= field(default_factory=StatusMaster)
    status : bool= field(default_factory=False)
    message : str= field(default_factory="Not info")

    