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
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return True
        except Exception as e:
            print(f'An error occurred while writing to the file: {e}')
            return False
    
    @staticmethod
    def file_exists(file_path):
        return os.path.exists(file_path)