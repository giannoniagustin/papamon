
import os
from util import File
class ImageController:
    @staticmethod
    def save(imageFile:str,content: bytes, createFolder=True):
        try:
            if (createFolder):
                 folder = os.path.dirname(imageFile)
                 File.FileUtil.createFolder(folder)  # Asegurarse de que la carpeta y las subcarpetas existan    
                        
            File.FileUtil.writeImage(imageFile,content)
            print("image save successfully. ")
        except FileNotFoundError as e:
                print("An error occurred when image save:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when image save:", e)
                raise

                
    @staticmethod
    def extract(imageFile:str,content: bytes, createFolder=True):
        try:
            if (createFolder):
                 folder = os.path.dirname(imageFile)
                 File.FileUtil.createFolder(folder)  # Asegurarse de que la carpeta y las subcarpetas existan    
                        
            File.FileUtil.extractFile(imageFile,content)
            print("image save successfully. ")

        except FileNotFoundError as e:
                print("An error occurred when image extract:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when image extract:", e)
                raise

