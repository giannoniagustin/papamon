import io
import os
import json
import platform
import subprocess
import zipfile
from io import BytesIO

from model.ListFiles import ListFiles
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
    def openFile(file_path,mode='r'):
         content = {}
         try:   
            with open(file_path, 'r') as file:
                return file
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
    def writeFile(file_path, content,mode='w'):
         try:   
            print('File path write: '+file_path)
            with open(file_path, mode) as file:
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
    def checkIfFilesExists(*files):
        result=True
        for file in files:
            if not FileUtil.fileExists(file):
                print(f"El archivo '{file}' no existe.")
                result= False
        return result
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
    @staticmethod
    def zipFile(filePath):
              try:
                     print("zipFoler: " + filePath)
                     # Crear un archivo ZIP en memoria
                     buffer = io.BytesIO()
                     with zipfile.ZipFile(buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
                            # Obtener la ruta relativa del archivo desde una carpeta base
                            rel_path = os.path.relpath(filePath, os.path.dirname(filePath))
                            # Agregar el archivo al ZIP con la ruta relativa para mantener la estructura
                            zipf.write(filePath, rel_path)

                     return buffer
              except Exception as e:
                     print("An error occurred when zipFile: ", e)
                     raise
    @staticmethod
    def isValidZip(bytes_io):
              try:
                     # Posiciona el objeto BytesIO al principio
                     bytes_io.seek(0)
                     # Intenta abrir el BytesIO como un archivo ZIP en modo lectura
                     with zipfile.ZipFile(bytes_io, 'r') as zip_ref:
                     # No se necesita hacer nada, solo queremos verificar si se puede abrir
                            return True
              except zipfile.BadZipFile:
                     # El objeto BytesIO no contiene un archivo ZIP válido
                     print(f"El objeto BytesIO no contiene un archivo ZIP válido")
                     return False
              except UnicodeDecodeError:
                     # El archivo ZIP en el objeto BytesIO contiene caracteres no válidos en la codificación
                     print(f"El archivo ZIP en el objeto BytesIO contiene caracteres no válidos en la codificación")

                     return False
              except Exception as e:
                     # Otros errores inesperados
                     print(f"Error al abrir el archivo ZIP desde BytesIO: {e}")
                     return False

    @staticmethod
    def listFolders(folderPath):
       print(f"Carpeta a listar: {folderPath}") # Ruta de la carpeta que deseas listar
       # Determinar el sistema operativo
       if platform.system() == "Windows":
              # Ejecutar el comando "dir" en Windows
              cmd = ["dir", folderPath]
       else:
       # Ejecutar el comando "ls" en sistemas tipo Unix (Linux)
              cmd = ["ls", folderPath]

       # Ejecutar el comando y capturar la salida
       try:
              result = subprocess.run(cmd, capture_output=True, text=True, check=True)
              print("Contenido de la carpeta:")
              print(result.stdout)
       except subprocess.CalledProcessError as e:
              print(f"Error al listar la carpeta: {e}")
       except FileNotFoundError:
              print("El comando 'ls' o 'dir' no está disponible en este sistema.")
              
    @staticmethod
    def getFiles(directory):
              try:
                     # Obtener la lista de elementos (archivos y carpetas) en el directorio
                     items = os.listdir(directory)
                     # Separar elementos en archivos y carpetas
                     files =[item for item in items if os.path.isfile(os.path.join(directory, item))]
                     folders = [item for item in items if os.path.isdir(os.path.join(directory, item))]
                     return {
                     "files": files,
                     "folders": folders}
                     
              except FileNotFoundError:
                     return None
              except Exception as e:
                     print(f"Error al listar la carpeta: {e}")
                     return None


