import os
import json
import zipfile
from io import BytesIO
class FileUtil:
     #Parsea a JSON , ver si hay otro tipo de archivo 
    @staticmethod
    def readFile(file_path):
         content = {}
         try:   
            with open(file_path, 'r') as file:
                content = json.load(file)
                return content
         except FileNotFoundError as e:
                print("An error File Not Found", e)
                raise
         except IOError as e:
                print("An error IOError", e)
                raise
         except Exception as e:
                print("An error occurred :", e)
                raise
    
    
    @staticmethod
    def writeFile(file_path, content):
         try:   
            print('File path write: '+file_path)
            with open(file_path, 'w') as file:
                file.write(content)
                return True
         except FileNotFoundError as e:
                print("An error File Not Found", e)
                return False
         except IOError as e:
                print("An error IOError", e)
                return False
         except Exception as e:
                print("An error occurred :", e)
                return False
    @staticmethod
    def writeImage(file_path, content):
            print('File path write: '+file_path)
            with open(file_path, "wb") as f:
                    f.write(content)
            return True
    
    @staticmethod
    def extractFile(file_path, content):
         try:   
            print('File path extract: '+file_path)
            # Descomprimir el archivo ZIP
            with zipfile.ZipFile(BytesIO(content), 'r') as zip_ref:
                    zip_ref.extractall(file_path)
                    return True
         except FileNotFoundError as e:
                print("An error File Not Found", e)
                return False
         except IOError as e:
                print("An error IOError", e)
                return False
         except Exception as e:
                print("An error occurred :", e)
                return False
    
    @staticmethod
    def fileExists(file_path):
        return os.path.exists(file_path)
    
    @staticmethod
    def createFolder(folder):
       if not os.path.exists(folder):    
        os.makedirs(folder)
        print(f"Carpeta '{folder}' creada exitosamente.")
       else:
        print(f"Carpeta '{folder}' ya existe.") 
    @staticmethod
    def filePath(file:str):
    # Obtener el directorio del archivo
       return os.path.dirname(file)

