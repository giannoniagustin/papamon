#DAR PERMISOS EN LINUX PARA LOS ARCHIVOS Y CARPETAS PORQUE SINO DICE ARCHVIO NOT FOUND
import os

# Obtiene la ruta de la carpeta 'Documents' del usuario
documents_folder = os.path.expanduser("~/Documents")
DATA_FOLDER = 'data'
RB_FOLDER = 'rb'
#CONFIG
CONFIG_FOLDER='config'
MASTER_FOLDER='master'
SLAVE='slave'

FIREBASE_FOLDER = 'firebase'
ME_SLAVE_FILE='me.json'
ME_MASTER_FILE='me.json'
SCHEDULER_STATUS_FILE='scheduler.json'
SCHEDULER_GET_IMAGES_FILE='schedulerGetImages.json'
SCHEDULER_GET_IMAGES_FILE_EXAMPLE='schedulerGetImages.json.example'


RASPBERRIES_FILE = 'raspberries.json'
FIREBASE_FILE = 'papamon-78c6c-firebase-adminsdk-9jlm9-71107c9a98.json'

ME_SLAVE =os.path.join(CONFIG_FOLDER,SLAVE,ME_SLAVE_FILE)
ME_MASTER=os.path.join(CONFIG_FOLDER,MASTER_FOLDER,ME_MASTER_FILE)
RASPBERRY = os.path.join(CONFIG_FOLDER,MASTER_FOLDER,RASPBERRIES_FILE)

SCHEDULER_STATUS=os.path.join(CONFIG_FOLDER,MASTER_FOLDER,SCHEDULER_STATUS_FILE)
SCHEDULER_GET_IMAGES=os.path.join(CONFIG_FOLDER,MASTER_FOLDER,SCHEDULER_GET_IMAGES_FILE)
SCHEDULER_GET_IMAGES_EXAMPLE=os.path.join(CONFIG_FOLDER,MASTER_FOLDER,SCHEDULER_GET_IMAGES_FILE_EXAMPLE)

FIREBASE = os.path.join(CONFIG_FOLDER,FIREBASE_FOLDER,FIREBASE_FILE)

#RB STATUS
STATUS_FILE = 'status.json'
STATUS_FILE_EXAMPLE = 'status.json.example'

STATUS_RB=os.path.join(DATA_FOLDER, RB_FOLDER,STATUS_FILE)
STATUS_RB_EXAMPLE=os.path.join(DATA_FOLDER, RB_FOLDER,STATUS_FILE_EXAMPLE)

#System STATUS
SYSTEM_STATUS_FILE = 'systemStatus.json'
SYSTEM_STATUS_FILE_EXAMPLE = 'systemStatus.json.example'
SYSTEM_STATUS=os.path.join(DATA_FOLDER, MASTER_FOLDER,SYSTEM_STATUS_FILE)
SYSTEM_STATUS_EXAMPLE=os.path.join(DATA_FOLDER, MASTER_FOLDER,SYSTEM_STATUS_FILE_EXAMPLE)

#IMAGES
#Folder
IMAGES=os.path.join(documents_folder, 'out_reconstruct')+os.sep#documents_folder+'reconstruct'+os.sep
BUILD_IMAGE_FOLDER=IMAGES+"{}" # 1 id_rquest
   #Builded Image 
BUILD_IMAGE_FILE=IMAGES+"{}"+os.sep+"{}"+os.sep+"{}"+"{}" # 1 id_request,2 id_rb, 3 id_request, 4 Extension file 
RECONSTRUCTION_OUT_FILE=os.sep+"reconstruction.json"

#MASTER PATHS
#RASPBERIES  STATUS
STATUS_RASPBERIES_FILE = 'statusRaspberies.json'
STATUS_RASPBERIES=os.path.join(DATA_FOLDER,MASTER_FOLDER, RB_FOLDER,STATUS_RASPBERIES_FILE)

#Extensions
JPG = ".jpg"
PNG = ".png"
ZIP = ".zip"
JSON = ".json"


DEPTH_FILE = 'depth.png'
POINT_FILE = 'points.csv'
RGB_FILE = 'rgb.png'