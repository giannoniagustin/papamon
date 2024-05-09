
from io import BytesIO
import os
import zipfile

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

    @staticmethod
    def extractMemory(folderPath:str,content: BytesIO, createFolder=True):
        try:
                if (File.FileUtil.isValidZip(content)):
                        print(f"Create folder path {folderPath}")
                        if (createFolder):
                                
                                folder = os.path.dirname(folderPath)
                                File.FileUtil.createFolder(folder)  # Asegurarse de que la carpeta y las subcarpetas existan    

                        with zipfile.ZipFile(content, "r") as zip_ref:
                                for file_info in zip_ref.infolist():
                                # Extrae el archivo actual del ZIP
                                        extracted_data = zip_ref.read(file_info.filename)
                                        # Construye la ruta completa de destino para guardar el archivo
                                        destino = os.path.join(folderPath, file_info.filename)

                                        # Asegúrate de que la carpeta de destino exista
                                        os.makedirs(os.path.dirname(destino), exist_ok=True)

                                        # Guarda el archivo en la ubicación de destino
                                        with open(destino, "wb") as archivo_destino:
                                                archivo_destino.write(extracted_data)

                                        print(f"Archivo {file_info.filename} guardado en {destino}")

                        print("Descompresión exitosa del archivo ZIP y archivos guardados en la ubicación de destino")
                else:
                        raise Exception("El archivo ZIP no es válido.") 

        except Exception as e:
                print("Error al descomprimir el archivo ZIP o al guardar los archivos en la ubicación de destino",e)
                print(f"Folder path {folderPath}")
                raise