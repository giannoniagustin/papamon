#!/bin/bash
# Script para configurar el servicio de PapamonApp Slave
# Autor: Papamon
# Ejemplo de uso: sudo ./configService.sh -name [nombre_servicio] [start|stop]

directorio="/home/papamon/Documents/papamon"
directorio_service="$directorio/config/service"
directorio_systemd="/etc/systemd/system"
nombre_servicio="No seteado"  # Nombre del archivo de servicio

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
if get_name_param "$@"; then
echo "Configurando el servicio PapamonApp $nombre_servicio"

if  has_start_param  "$@" ; then
    echo "Configurando Inicio de servicio PapamonApp $nombre_servicio"

    # Llama al script para buildear
    echo "Buildeando Apps"
    sudo ./configAllBuild.sh

    # Llama al script configCopyService.sh con los parámetros fijos
    sudo ./configCopyService.sh "$directorio_service/$nombre_servicio" "$directorio_systemd"
    sudo systemctl daemon-reload
    if [ "$nombre_servicio" != "syncRClone.service" and "$nombre_servicio" != "papamonSyncApp.service" ]; then
    sudo systemctl stop $nombre_servicio
    sudo systemctl enable $nombre_servicio
    sudo systemctl start  $nombre_servicio
    #sudo systemctl status $nombre_servicio
    fi
elif has_stop_param  "$@"; then
    echo "Configurando Detencion de servicio PapamonApp $nombre_servicio"
    sudo systemctl stop $nombre_servicio
    sudo systemctl disable $nombre_servicio
    #sudo systemctl status $nombre_servicio
fi
else
    echo "No se ha proporcionado el parametro -name"
fi

