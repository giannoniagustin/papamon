from dataclasses import dataclass,field
from model.Raspberry import Raspberry
from model.StatusSlave import StatusSlave
@dataclass
class StatusSystem:
    slaves :list[Raspberry] = field(default_factory=list)
    slaveStatus: list[StatusSlave]= field(default_factory=list)
    status : bool= field(default_factory=False)
    message : str= field(default_factory="Not info")

    