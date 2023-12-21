import urllib.request
class Util:
    @staticmethod
    def checkInternetConnection()->bool:
        try:
            urllib.request.urlopen('https://www.google.com', timeout=30) # Intenta acceder a Google
            print("¡Conexión a Internet establecida!")
            return True
        except urllib.error.URLError:
            print("No hay conexión a Internet.")
            return False
        except Exception as e:
            print("Error al verificar la conexión a Internet: ", e)
            return False

