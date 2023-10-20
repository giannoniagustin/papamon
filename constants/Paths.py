#DAR PERMISOS EN LINUX PARA LOS ARCHIVOS Y CARPETAS PORQUE SINO DICE ARCHVIO NOT FOUND
import os

# Obtiene la ruta de la carpeta 'Documents' del usuario
documents_folder = os.path.expanduser("~/Documents")
DATA_FOLDER = 'data'
RB_FOLDER = 'rb'
#CONFIG
CONFIG_FOLDER='config'
MASTER_FOLDER='master'
FIREBASE_FOLDER = 'firebase'
ME_FILE='me.json'
SCHEDULER_FILE='scheduler.json'
RASPBERRY_FILE = 'raspberry.json'
FIREBASE_FILE = 'papamon-78c6c-firebase-adminsdk-9jlm9-71107c9a98.json'

ME =os.path.join(CONFIG_FOLDER,ME_FILE)
RASPBERRY = os.path.join(CONFIG_FOLDER,MASTER_FOLDER,RASPBERRY_FILE)
SCHEDULER=os.path.join(CONFIG_FOLDER,MASTER_FOLDER,SCHEDULER_FILE)
FIREBASE = os.path.join(CONFIG_FOLDER,FIREBASE_FOLDER,FIREBASE_FILE)

#RB STATUS
STATUS_FILE = 'status.json'
STATUS_RB=os.path.join(DATA_FOLDER, RB_FOLDER,STATUS_FILE)

#IMAGES
#Folder
IMAGES=os.path.join(documents_folder, 'reconstruct')+os.sep#documents_folder+'reconstruct'+os.sep
BUILD_IMAGE_FOLDER=IMAGES+"{}" # 1 id_rquest
   #Builded Image 
BUILD_IMAGE_FILE=IMAGES+"{}"+os.sep+"{}"+os.sep+"{}"+"{}" # 1 id_request,2 id_rb, 3 id_request, 4 Extension file 


#MASTER PATHS
#RASPBERIES  STATUS
STATUS_RASPBERIES_FILE = 'statusRaspberies.json'

STATUS_RASPBERIES=os.path.join(DATA_FOLDER,MASTER_FOLDER, RB_FOLDER,STATUS_RASPBERIES_FILE)

#Extensions
JPG = ".jpg"
PNG = ".png"
ZIP = ".zip"


DEPTH_FILE = 'depth.png'
POINT_FILE = 'points.csv'