#!/bin/bash
# Script para  habilitarPapamonApp Master
# Autor: Agustin Giannoni
# Ejemplo de uso: sudo ./slave.sh start|stop


papamonAppService="papamonApp.service"
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

if  has_start_param  "$@" ; then
    echo "Configurando Inicio de Slave"
    #Start Service
    sudo ./configService.sh -name "$papamonAppService" start

    fi
elif has_stop_param  "$@"; then
    echo "Configurando Detencion de Slave"
    #Stop Service
    sudo ./configService.sh -name "$papamonAppService" stop
fi








