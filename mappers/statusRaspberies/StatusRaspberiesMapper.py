from dataclasses import asdict
from model.StatusRaspberies import StatusRaspberies
import json

class StatusRaspberiesMapper:

    def toStatusRaspberies( self,dictFile: dict)-> StatusRaspberies :
        instance = StatusRaspberies(**dictFile)
        return instance
    
    def toStatusRaspberiesList( self,dictFile: dict)-> list[StatusRaspberies] :
        print("Parseando toStatusRaspberiesList")
        # Crear lista de objetos Persona
        listObjects = []
        for objectJson in dictFile:
            instance=self.toStatusRaspberies(objectJson)
            print(f"Status Raspberies {instance}")
            listObjects.append(instance)
        return listObjects
    
    def toJson( self,dictFile: StatusRaspberies) :
        # Convert Persona instance to dictionary and then to JSON
        objectDict = asdict(dictFile)
        objectJson = json.dumps(objectDict, indent=4)
        print('StatusRaspberies to Json --'+objectJson)
        return objectJson
    def toJsonList( self,dictFile: list[StatusRaspberies]) :
        # Convert Persona instance to dictionary and then to JSON
        objectDict = [asdict(obj) for obj in dictFile]
        objectJson = json.dumps(objectDict, indent=4)
        print('List StatusRaspberies to Json --'+objectJson)
        return objectJson
