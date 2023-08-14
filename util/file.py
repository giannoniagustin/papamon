import os
import json
class FileUtil:
     #Parsea a JSON , ver si hay otro tipo de archivo 
    @staticmethod
    def read_file(file_path):
            with open(file_path, 'r') as file:
                content = json.load(file)
                return content
    
    @staticmethod
    def write_file(file_path, content):
      #  try:
            print('File path write: '+file_path)
            with open(file_path, 'w') as file:
                file.write(content)
            return True
    
    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)
    @staticmethod
    def createFolder(folder):
        os.mkdir(folder)
        print(f"Carpeta '{folder}' creada exitosamente.")