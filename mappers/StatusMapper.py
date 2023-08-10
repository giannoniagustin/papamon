from dataclasses import dataclass, make_dataclass

class StatusMapper:

    def toStatus( self,dictFile: dict) :
        from model.Status import Status
        Status = make_dataclass("Status", dictFile.keys())
        instance = Status(**dictFile)
        return instance