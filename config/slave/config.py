from model.Raspberry import Raspberry
from controllers.raspberry.RaspberryController import RaspberryController

meRaspb: Raspberry = RaspberryController.getMe()
#programsaveCam = "./rs-save-cam-status"
programsaveCam = "rs-save-cam-status.exe"
reconstructFolder= "reconstruct"
isDemo =True
version = "Slave 1.0"