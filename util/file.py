import os
import json
class FileUtil:
     #Parsea a JSON , ver si hay otro tipo de archivo 
    @staticmethod
    def readFile(file_path):
            with open(file_path, 'r') as file:
                content = json.load(file)
                return content
    
    @staticmethod
    def writeFile(file_path, content):
            print('File path write: '+file_path)
            with open(file_path, 'w') as file:
                file.write(content)
            return True
    @staticmethod
    def writeImage(file_path, content):
            print('File path write: '+file_path)
            with open(file_path, "wb") as f:
                    f.write(content)
            return True
    
    @staticmethod
    def fileExists(file_path):
        return os.path.exists(file_path)
    
    @staticmethod
    def createFolder(folder):
        os.mkdir(folder)
        print(f"Carpeta '{folder}' creada exitosamente.")