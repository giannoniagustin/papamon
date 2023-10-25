from model.Raspberry import Raspberry
from controllers.raspberry.RaspberryController import RaspberryController

meRaspb: Raspberry = RaspberryController.getMe()
programsaveCam = ""
programsaveCam_Linux = "./rs-reconstruct"
programsaveCam_Win = "rs-reconstruct.exe"
reconstructFolder= "reconstruct"
isDemo =False
version = "Master 1.0"
SO=""
