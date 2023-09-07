
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
import constants.Paths as Paths
# Add an attachment
from sentry_sdk import configure_scope

class Sentry:
        @staticmethod
        def init():
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
                debug=True,  # Habilita el modo de depuración (opcional)
                ) 
            sentry_sdk.capture_message("Inicio de Sentry") 

        @staticmethod
        def customMessage(filename:str,path:str,eventName:str):
                with sentry_sdk.configure_scope() as scope:
                    scope.add_attachment(filename=filename,path=path)
                    sentry_sdk.capture_message(eventName) 
                    scope.clear()   

     
