
from util import File
class ImageController:
    @staticmethod
    def save(imageFile:str,content: bytes):
        try:
            File.FileUtil.writeImage(imageFile,content)
        except FileNotFoundError as e:
                print("An error occurred when image save:", e)
                raise
        except IOError as e:
                raise
        except Exception as e:
                print("An error occurred when image save:", e)
                raise
        else:
                print("image save successfully. ")
