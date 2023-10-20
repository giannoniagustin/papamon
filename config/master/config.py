from model.Raspberry import Raspberry
from controllers.raspberry.RaspberryController import RaspberryController

meRaspb: Raspberry = RaspberryController.getMe()
programsaveCam = "./rs-save-cam-status"
reconstructFolder= "reconstruct"
isDemo =True