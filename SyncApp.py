#!/usr/bin/env python3
import os
import sys
import requests
import constants.Paths as Paths
from util.Sentry import Sentry
from util import File
from util.Parser import Parser
from util.Util import Util
import config.sync.config as config
import config.master.config as MasterConfig
isDemo=False
def initApp():
    Sentry.init()               
    print(os.linesep+"#################################################################"+os.linesep)
    print(f"Inicio de SyncApp   "+os.linesep)
    configParameter()
    

def configParameter():
    print(os.linesep+"#########################CONFIGURATIONS########################################"+os.linesep)
    if "-demo" in sys.argv:
        print("El parámetro '-demo' está presente.")
        global isDemo
        isDemo=True

def sentFiles(ruta_base):
    sentFiles = loadSentFiles()
    newSentFiles = set()
    for ruta_actual,carpetas,archivos in os.walk(ruta_base):
        for fileName in archivos:
            if fileName == Paths.RECONSTRUCTION_FILE:
                print(f"Procesando archivo {fileName}...")
                fullFilePath = os.path.join(ruta_actual, fileName)
                # Verificar si el archivo ya ha sido enviado previamente
                if fullFilePath not in sentFiles:
                    try:
                        print(f"Enviando archivo {fullFilePath} a  Backend...")
                        sendToBackend(fullFilePath,fileName)
                        print(f"Archivo {fullFilePath} enviado a Backend.")
                        # Agregar el archivo a la lista de enviados
                        newSentFiles.add(fullFilePath)
                    except Exception as e:
                        print(f"Error al enviar el archivo {fullFilePath} a Sentry: {e}")
                else:
                    #print(f"El archivo {fullFilePath} ya ha sido enviado previamente.")
                    pass
    saveSentFiles(newSentFiles)
def saveSentFiles(archivos_enviados):
    syncSendFile = Paths.SYNC_SEND_FILE
    File.FileUtil.createFolder(File.FileUtil.filePath(syncSendFile))
    try:
        with open(syncSendFile, 'a') as file:
            # Guardar cada nombre de archivo en una línea separada en el archivo
            for line in archivos_enviados:
                #file.write(nombre_archivo + '\n')
                File.FileUtil.writeFile(syncSendFile,line + '\n',mode='a')
    except IOError as e:
        print(f"Error al guardar archivos enviados: {e}")
def loadSentFiles():
    syncSendFile = Paths.SYNC_SEND_FILE
    sentFiles = set()
    File.FileUtil.createFolder(File.FileUtil.filePath(syncSendFile))
    try:
        if not File.FileUtil.fileExists(syncSendFile):
            File.FileUtil.writeFile(syncSendFile, "")
        with open(syncSendFile, 'r') as file:
            for line in file:
                # Agregar cada nombre de archivo a un conjunto
                sentFiles.add(line.strip())  # Elimina los espacios en blanco alrededor del nombre del archivo si los hay
    except Exception as e:
        # Manejar el caso donde el archivo de registros aún no existe
        print(f"Error al cargar archivos enviados: {e}")
        raise
    return sentFiles
def sendToBackend(file:str,filename:str=""):
   sendToSentry(file,filename)
   #sendToFirestore(file,filename)
   print("sendToBackend")

def sendToSentry(file:str,filename:str=""):
    global isDemo
    nameEvent="Reconstrucción de imagen"
    filename =MasterConfig.meRaspb.name+"-"+file
    if Util.checkInternetConnection():
        if isDemo:
          nameEvent=f"{nameEvent} Demo" 
          Sentry.sendFile(filename=filename,path=file,eventName=f"{nameEvent}")

        else:
          Sentry.sendFile(filename=filename,path=file,eventName=f"{nameEvent}")
        
    else:
         raise Exception("No hay conexión a Internet.")
def sendToFirestore(file:str,filename:str="")->bool:
            sendSuccess = False
            try:
                url= config.reconstructionUrl
                print("Url firebase ",url)
                # Leer el contenido del archivo
                json_file_content = File.FileUtil.readFile(file)
                json_file = Parser.toJson(json_file_content)
                # Configurar los encabezados para indicar que estás enviando un JSON
                headers = {'Content-Type': 'application/json'}
                # Realizar la solicitud POST con el JSON
                response = requests.post(url, data=json_file, headers=headers)
                if response.status_code == 200:
                    print(f"Archivo enviado a Firebase: {response.status_code}")
                    sendSuccess = True
                else:
                    print(f"Error al enviar archivo a Firebase: {response.status_code}")
                    raise Exception(f"Error al enviar archivo a Firebase: {response.status_code}")
            except requests.exceptions.ConnectionError as e:
                    print("Error de conexión:", e)
                    Sentry.captureException(e)
                    raise  Exception(e)
            except requests.exceptions.RequestException as e:
                    print("Error en la solicitud:", e)
                    Sentry.captureException(e)
                    raise  Exception(e)

            except Exception as e:
                    print("Error al enviar archivo a Firebase", e)
                    Sentry.captureException(e)
                    raise
            finally:
                    return sendSuccess
if __name__ == "__main__":
    try:
        initApp()
        sentFiles(Paths.IMAGES)
    except Exception as e:
        print("Error en la aplicación:", e)



    

