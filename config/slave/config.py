from model.Raspberry import Raspberry
from controllers.raspberry.RaspberryController import RaspberryController

meRaspb: Raspberry = RaspberryController.getMe()
programsaveCam = "./rs-save-cam-status"
programsaveCam_Win = "rs-save-cam-status.exe"
programsaveCam_Linux = "./rs-save-cam-status"

reconstructFolder= "reconstruct"
isDemo =False
SO=""
version = "Slave 1.0"