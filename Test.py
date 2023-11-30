
import constants.Paths as Paths
import datetime
import os

def createFolder(folder):
    try:      
        if not os.path.exists(folder):    
            os.makedirs(folder, exist_ok=True)
            with open('/home/papamon/Documents/papamon/log.txt', 'a') as log_file:
                log_file.write(f"Carpeta '{folder}' creada exitosamente.\n")
        else:
            with open('/home/papamon/Documents/papamon/log.txt', 'a') as log_file:
                log_file.write(f"Carpeta '{folder}' ya existe.\n") 
    except Exception as e:
        with open('/home/papamon/Documents/papamon/log.txt', 'a') as log_file:
            log_file.write(f"An error occurred when creating folder '{folder}': {e}\n")
        raise

createFolder(Paths.BUILD_IMAGE_FOLDER.format(datetime.datetime.now()))
