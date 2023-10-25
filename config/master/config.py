from model.Raspberry import Raspberry
from controllers.raspberry.RaspberryController import RaspberryController

meRaspb: Raspberry = RaspberryController.getMe()
programsaveCam = "./rs-reconstruct"
reconstructFolder= "reconstruct"
isDemo =True
version = "Master 1.0"
SO=""
