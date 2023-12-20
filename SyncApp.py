#!/usr/bin/env python3
import os
import constants.Paths as Paths
from util.Sentry import Sentry
from util import File

def initApp():
    print(os.linesep+"#################################################################"+os.linesep)
    print(f"Inicio de SyncApp   "+os.linesep)
    configParameter()

def configParameter():
    print(os.linesep+"#########################CONFIGURATIONS########################################"+os.linesep)

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
                    print(f"El archivo {fullFilePath} ya ha sido enviado previamente.")
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
    return sentFiles
def sendToBackend(file:str,filename:str=""):
   # sendToSentry(file,filename)
   print("sendToBackend")

def sendToSentry(file:str,filename:str=""):
    Sentry.init()   
                        
    Sentry.sendFile(filename=filename,path=file,eventName=f"Historial de Reconstruccion")

if __name__ == "__main__":
    initApp()
    sentFiles(Paths.IMAGES)



    

