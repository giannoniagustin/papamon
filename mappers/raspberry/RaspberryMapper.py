from model.Raspberry import Raspberry

class RaspberryMapper:

    def toRaspberies( self,dictFile: dict)-> list[Raspberry] :
        print("Parseando toRaspberies")
        # Crear lista de objetos Persona
        listRaspberry = []
        for objectJson in dictFile:
            instance=self.toRaspberry(objectJson)
            print(f"Instancia raspberry {instance}")
            listRaspberry.append(instance)
        return listRaspberry
    
    def toRaspberry( self,dictFile: dict)->Raspberry :
        instance = Raspberry(**dictFile)
        return instance