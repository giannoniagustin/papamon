import io
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
    def isFileEmpty(pathFile):
       try:
              with open(pathFile, 'r') as archivo:
                     contenido = archivo.read()
                     return len(contenido) == 0
       except FileNotFoundError:
              print(f"El archivo '{pathFile}' no existe.")
              return False
       
    @staticmethod
    def createIsFileEmptyOrNotExist(path,fileExample):
      try:     
              if (FileUtil.isFileEmpty(path) or  not FileUtil.fileExists(path)):
                FileUtil.writeFile(path,fileExample)
      except Exception as e:
              print("An error occurred when isFileEmptyOrNotExist: ",e)
              raise
          
    @staticmethod
    def createFolder(folder):
       try:      
              if not os.path.exists(folder):    
                     os.makedirs(folder,exist_ok=True)
                     print(f"Carpeta '{folder}' creada exitosamente.")
              else:
                     print(f"Carpeta '{folder}' ya existe.") 
       except Exception as e:
                     print(f"An error occurred when create folder '{folder}' : ",e)
                     raise
              
    @staticmethod
    def filePath(file:str):
    # Obtener el directorio del archivo
       return os.path.dirname(file)
    @staticmethod
    def zipFoler(folderPath):
     try:        
        print("zipFoler: "+folderPath)    
    # Crear un archivo ZIP en memoria
        buffer = io.BytesIO()
        with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(folderPath):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Agregar el archivo al archivo ZIP con una ruta relativa
                    zipf.write(file_path, os.path.relpath(file_path, folderPath))

        # Preparar la respuesta
        buffer.seek(0)
        return buffer
     except Exception as e:
              print("An error occurred when zipFoler: ",e)
              raise




