from dataclasses import asdict
from model.ListFiles import ListFiles
from util.Parser import Parser

class ListFileMapper:

    def toListFile( self,dictFile: dict) :
        instance = ListFiles(**dictFile)
        return instance
    
    def toJson( self,instanceObject: ListFiles) :
        # Convert  instance to dictionary and then to JSON
        jsonObject =Parser.toJson(instanceObject)
        return jsonObject
