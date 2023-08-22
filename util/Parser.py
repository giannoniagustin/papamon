
import json
class Parser:
    
    @staticmethod
    def toDict(obj):
        if isinstance(obj, list):
            return [Parser.toDict(item) for item in obj]
        elif hasattr(obj, '__dict__'):
            return {key: Parser.toDict(value) for key, value in obj.__dict__.items()}
        else:
            return obj
    @staticmethod
    def toJson(instance:object):
        dictObject =Parser.toDict(instance)
        jsonObject = json.dumps(obj=dictObject, indent=4)
        return jsonObject
