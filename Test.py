#!/usr/bin/env python3
from model.StatusSlave import StatusSlave
from model.Raspberry import Raspberry
from model.Status import Status
from model.StatusSystem import StatusSystem


from dataclasses import dataclass

@dataclass
class Address:
    street: str
    city: str

@dataclass
class Person:
    name: str
    age: int
    address: Address

@dataclass
class Company:
    name: str
    employees: list

def to_dict(obj):
    if isinstance(obj, list):
        return [to_dict(item) for item in obj]
    elif hasattr(obj, '__dict__'):
        return {key: to_dict(value) for key, value in obj.__dict__.items()}
    else:
        return obj
# Crear instancias de Address, Person y Company
statusRb1 =StatusSlave(raspberry=Raspberry("a","b","c","s"),status=Status(True,"ssss"))
statusRb2 =StatusSlave(raspberry=Raspberry("a","b","c","s"),status=Status(True,"ssss"))
statusRb3 =StatusSlave(raspberry=Raspberry("a","b","c","s"),status=Status(True,"ssss"))
lista: List[StatusSlave]=[]
lista.append(statusRb1)
lista.append(statusRb2)
lista.append(statusRb3)

statusSystem= StatusSystem(slaves=lista,status=True)

# Serializar objetos a diccionarios
address_dict = to_dict(statusSystem)


print(address_dict)

