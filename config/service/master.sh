#!/bin/bash
# Script para  habilitarPapamonApp Master
# Autor: Agustin Giannoni
# Ejemplo de uso: sudo ./master.sh start|stop


papamonMasterAppService="papamonMasterApp.service"  
papamonCheckStatusAppService="papamonCheckStatusApp.service"  
syncRCloneService="syncRClone.service"  
syncRCloneTimer="syncRClone.timer"  
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
    echo "Configurando Inicio de Master"
    #Start Service
    sudo ./configService.sh -name "$papamonCheckStatusAppService" start
    sudo ./configService.sh -name "$syncRCloneService" start
    sudo ./configService.sh -name "$syncRCloneTimer" start
elif has_stop_param  "$@"; then
    echo "Configurando Detencion de Master"
    #Stop Service
    sudo ./configService.sh -name "$papamonCheckStatusAppService" stop
    sudo ./configService.sh -name "$syncRCloneService" stop
    sudo ./configService.sh -name "$syncRCloneTimer" stop
fi








