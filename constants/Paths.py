#DAR PERMISOS EN LINUX PARA LOS ARCHIVOS Y CARPETAS PORQUE SINO DICE ARCHVIO NOT FOUND
import os


#CONFIG
CONFIG_FOLDER='config'
ME_FILE='me.json'
ME =os.path.join(CONFIG_FOLDER,ME_FILE)
RASPBERRY_FILE = 'raspberry.json'
RASPBERRY = os.path.join(CONFIG_FOLDER,RASPBERRY_FILE)


#RB STATUS
RB=os.path.join('data', 'rb','status.json')
STATUS_RB=os.path.join('data', 'rb','status.json')

#IMAGES
    #Folder
IMAGES='images'+os.sep
BUILD_IMAGE_FOLDER=IMAGES+"{}" # 1 id_rquest
   #Builded Image 
BUILD_IMAGE_FILE=IMAGES+"{}"+os.sep+"{}"+"-"+"{}"+"{}" # 1 id_rquest,2 id_rquest, 3 id_rb, 4 Extension file 

#MASTER PATHS
#RASPBERIES  STATUS
STATUS_RASPBERIES=os.path.join('data','master', 'rb','statusRaspberies.json')
