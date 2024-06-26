
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

class Sentry:
        @staticmethod
        def init():
            print(os.linesep+"#########################INIT SENTRY########################################"+os.linesep)
            sentry_sdk.init(
                dsn="https://907fed6f0f57920999ad05c29b8f74fa@o4505815265902592.ingest.sentry.io/4505815269113856",
                integrations=[FlaskIntegration()],
                # Set traces_sample_rate to 1.0 to capture 100%
                # of transactions for performance monitoring.
                # We recommend adjusting this value in production.
                traces_sample_rate=1.0,
                # Set profiles_sample_rate to 1.0 to profile 100%
                # of sampled transactions.
                # We recommend adjusting this value in production.
                profiles_sample_rate=1.0,
                debug=False,  # Habilita el modo de depuración (opcional)
                ) 
            # Habilita la integración de Sentry para multiprocessing
           # sentry_sdk.capture_message("Inicio de Sentry") 

        @staticmethod
        def customMessage(filename:str=None,path:str="",eventName:str=""):
                if (filename != None):
                    with sentry_sdk.configure_scope() as scope:
                        scope.add_attachment(filename=filename,path=path)
                        sentry_sdk.capture_message(eventName) 
                        scope.clear()
                else:
                        sentry_sdk.capture_message(eventName) 
      
        @staticmethod
        def sendFile(filename: str, path: str , eventName: str ):
            try:

                with sentry_sdk.configure_scope() as scope:
                    try:
                        scope.add_attachment(filename=filename, path=path)
                        sentry_sdk.capture_message(eventName)
                        scope.clear()
                    except Exception as e:
                        print(f"Error al enviar el evento a Sentry: {e}")
                        return False

                return True  # Devolver True si se envió exitosamente
            except Exception as e:
                print(f"Error al enviar el evento a Sentry: {e}")
                return False  # Devolver False si ocurrió un error durante el envío
        
        @staticmethod
        def captureException(e):
            sentry_sdk.capture_exception(e)
        

     
