
import multiprocessing
from util.Sentry import Sentry

class ProcessController:
    @staticmethod
    def run(proccesRun):
       
          # Crea un proceso secundario para ejecutar el planificador en segundo plano
        proceso_secundario = multiprocessing.Process(target=proccesRun)
        # Inicia el proceso secundario
        proceso_secundario.start()
