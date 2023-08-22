from dataclasses import dataclass
from model.Raspberry import Raspberry
from model.Status import Status
@dataclass
class StatusSystem:
    slaves :list[Raspberry] 
    status : bool
    def as_dict(self):
        return {
            "slaves": self.slaves.__dict__,
            "status": self.status.__dict__
        }
    

    