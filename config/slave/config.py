from model.Raspberry import Raspberry
from controllers.raspberry.RaspberryController import RaspberryController

meRaspb: Raspberry = RaspberryController.getMe()
programsaveCam = "./rs-save-cam-status"
programsaveCam_win = "rs-save-cam-status.exe"
reconstructFolder= "reconstruct"
isDemo =True
SO=""
version = "Slave 1.0"