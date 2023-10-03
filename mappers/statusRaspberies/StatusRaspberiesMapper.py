from model.StatusSlave import StatusSlave
from util.Parser import Parser
from typing import List
class StatusRaspberiesMapper:

    def toStatusRaspberies( self,dictFile: dict)-> StatusSlave :
        instance = StatusSlave(**dictFile)
        return instance
    
    def toStatusRaspberiesList( self,dictFile: dict)-> List[StatusSlave] :
        print("Parseando toStatusRaspberiesList")
        # Crear lista de objetos StatusRaspberies
        listObjects = []
        for objectJson in dictFile:
            instance=self.toStatusRaspberies(objectJson)
            print(f"Status Raspberies {instance}")
            listObjects.append(instance)
        return listObjects
    
    def toJson( self,instanceObject: StatusSlave) :
        # Convert StatusRaspberies instance to dictionary and then to JSON
        jsonObject = Parser.toJson(instanceObject)
        print('StatusRaspberies to Json --'+jsonObject)
        return jsonObject
    
    '''def toJsonList( self,instanceObject: List[StatusRaspberies]) :
        # Convert Persona instance to dictionary and then to JSON
        jsonObject = Parser.toJson(instanceObject)
        print('List StatusRaspberies to Json --'+jsonObject)
        return jsonObject'''
