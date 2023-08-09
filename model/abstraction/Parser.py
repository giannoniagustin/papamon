from abc import ABC, abstractmethod

class Parser(ABC):
    
    @abstractmethod
    def toJson(self):
        pass