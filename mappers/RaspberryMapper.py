from dataclasses import  make_dataclass

class RaspberryMapper:

    def toRaspberry( self,dictFile: dict) :
        from model.Me import Me
        # Crear lista de objetos Persona
        listRaspberry = []
        for objectJson in dictFile:
            id = objectJson["id"]
            name = objectJson["name"]
            ip = objectJson["ip"]
            print(f"ID: {id}, Name: {name}, IP: {ip}")
            Me = make_dataclass("Raspberry", objectJson.keys())
            instance = Me(**objectJson)
            listRaspberry.append(instance)
        return listRaspberry