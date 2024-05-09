#!/bin/bash
# Función para obtener el valor de -name si se proporciona
has_demo_param() {
    for var in "$@"; do
        if [ "$var" == "-demo" ]; then
            return 0
        fi
    done
    return 1
}

if ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
    # Ejecutar el comando si hay conexión a internet
        echo "Hay conexión a internet."
        if has_demo_param "$@"; then
            echo "Configurando Demo"
            mkdir -p /home/papamon/Documents/out_reconstruct_test/log/
            rclone --filter-from=/home/papamon/Documents/papamon/config/service/syncFilter.txt sync /home/papamon/Documents/out_reconstruct drive:/out_reconstruct_test -P -v --log-file /home/papamon/Documents/out_reconstruct/log/rclone_test.txt
            exit
        fi
        mkdir -p /home/papamon/Documents/out_reconstruct/log/
        rclone --filter-from=/home/papamon/Documents/papamon/config/service/syncFilter.txt sync /home/papamon/Documents/out_reconstruct drive:/out_reconstruct -P -v --log-file /home/papamon/Documents/out_reconstruct/log/rclone.txt
        exit

else
    # Puedes poner aquí un mensaje o alguna acción alternativa
    echo "No hay conexión a internet."
    exit
fi
