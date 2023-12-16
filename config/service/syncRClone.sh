#!/bin/bash

if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
    # Ejecutar el comando si hay conexión a internet
    echo "Hay conexión a internet."
    if pidof -o %PPID -x syncRClone.sh”; then
        echo "Ya se esta ejutando el script de una ejecucion anterior"
        exit 1
    else
        sudo rclone sync /home/papamon/Documents/out_reconstruct drive:/out_reconstruct -P
        file=/home/papamon/Documents/out_reconstruct/log/rclone.log -v 
fi
else
    # Puedes poner aquí un mensaje o alguna acción alternativa
    echo "No hay conexión a internet."
    exit

fi
