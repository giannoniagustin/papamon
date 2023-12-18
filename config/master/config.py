from model.Raspberry import Raspberry
from controllers.raspberry.RaspberryController import RaspberryController
import constants.Paths as Paths

meRaspb: Raspberry = RaspberryController.getMe(Paths.ME_MASTER)
programsaveCam = ""
programsaveCam_Linux = "./rs-reconstruct"
programsaveCam_Win = "rs-reconstruct.exe"
programNgrokUrl = "cicada-resolved-allegedly.ngrok-free.app"
#programNgrokUrl = "likely-liked-sawfly.ngrok-free.app"
reconstructFolder= "reconstruct"
isDemo =False
forceReconstruc = False
forceCheckStatus = False

version = "Master 1.0"
SO=""
