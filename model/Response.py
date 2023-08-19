from abc import ABC, abstractmethod
RESPONSE_OK=200

class AbstractResponse(ABC):
    def __init__(self, data=None, message=None):
        self.data = data
        self.message = message

    @abstractmethod
    def serialize(self):
        pass

class SuccessResponse(AbstractResponse):
    def serialize(self):
        return {
            "status": "success",
            "data": self.data,
            "message": self.message
        }

class ErrorResponse(AbstractResponse):
    def serialize(self):
        return {
            "status": "error",
            "data": self.data,
            "message": self.message
        }
