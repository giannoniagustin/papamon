#!/bin/bash
# Script para configurar el servicio de PapamonApp Slave
# Autor: Papamon

directorio="/home/papamon/Documents/papamon"
nombre_servicio="papamonApp.service"  # Nombre del archivo de servicio

# Función para obtener el valor de -name si se proporciona
get_name_param() {
    while [[ "$#" -gt 0 ]]; do
        if [ "$1" == "-name" ]; then
            nombre_servicio="$2"
            return 0
        fi
        shift
    done
    return 1
}

has_start_param() {
    for var in "$@"; do
        if [ "$var" == "start" ]; then
            return 0
        fi
    done
    return 1
}
has_stop_param() {
    for var in "$@"; do
        if [ "$var" == "stop" ]; then
            return 0
        fi
    done
    return 1
}
get_name_param "$@";then
echo "Configurando el servicio PapamonApp $nombre_servicio"

if  has_start_param  "$@" ; then
    echo "Configurando Inicio de servicio PapamonApp $nombre_servicio"
    sudo systemctl daemon-reload
    sudo systemctl stop $nombre_servicio
    sudo systemctl enable $nombre_servicio
    sudo systemctl start  $nombre_servicio
    sudo systemctl status $nombre_servicio
elif has_stop_param  "$@"; then
    echo "Configurando Detencion de servicio PapamonApp $nombre_servicio"
    sudo systemctl stop $nombre_servicio
    sudo systemctl disable $nombre_servicio
    sudo systemctl status $nombre_servicio
fi
else
    echo "No se ha proporcionado el parametro -name"
fi

