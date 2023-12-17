#!/bin/bash

if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
    # Ejecutar el comando si hay conexión a internet
        echo "Hay conexión a internet."
        mkdir -p /home/papamon/Documents/out_reconstruct/log/
        rclone sync /home/papamon/Documents/out_reconstruct drive:/out_reconstruct -P -v --log-file /home/papamon/Documents/out_reconstruct/log/rclone.txt
        exit

else
    # Puedes poner aquí un mensaje o alguna acción alternativa
    echo "No hay conexión a internet."
    exit
fi
