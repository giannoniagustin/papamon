import os
import json
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
    def fileExists(file_path):
        return os.path.exists(file_path)
    
    @staticmethod
    def createFolder(folder):
        os.mkdir(folder)
        print(f"Carpeta '{folder}' creada exitosamente.")
