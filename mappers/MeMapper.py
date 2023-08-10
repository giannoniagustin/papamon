from dataclasses import  make_dataclass

class MeMapper:

    def toMe( self,dictFile: dict) :
        from model.Me import Me
        Me = make_dataclass("Me", dictFile.keys())
        instance = Me(**dictFile)
        return instance