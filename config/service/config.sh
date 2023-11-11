#!/bin/bash
has_demo_param() {
    for var in "$@"; do
        if [ "$var" == "-demo" ]; then
            return 0
        fi
    done
    return 1
}
has_force_param() {
    for var in "$@"; do
        if [ "$var" == "-force" ]; then
            return 0
        fi
    done
    return 1
}


if [ "$1" == "slave" ]; then
    echo "Configurando el servicio PapamonApp Slave"
    sudo systemctl enable papamonApp.service
    sudo systemctl stop papamonMasterApp.service
    sudo systemctl disable papamonMasterApp.service
    sudo systemctl daemon-reload
    if has_demo_param "$@"; then
        echo "Modo demo "
        sudo systemctl start papamonApp.service
    else
        sudo systemctl start papamonApp.service
    fi

    echo "Estado servicio PapamonApp Slave"
    sudo systemctl status papamonApp.service
    echo "Estado servicio PapamonMasterApp Master"
    sudo systemctl status papamonMasterApp.service
elif [ "$1" == "master" ]; then
    echo "Configurando el servicio PapamonMasterApp Master.."
    sudo systemctl enable papamonMasterApp.service
    sudo systemctl stop papamonApp.service
    sudo systemctl disable papamonApp.service
    sudo systemctl daemon-reload
    if has_force_param "$@"; then
        sudo systemctl start papamonMasterApp.service
    else
        sudo systemctl start papamonMasterApp.service
    fi

    echo "Estado servicio PapamonApp Slave"
    sudo systemctl status papamonApp.service
    echo "Estado servicio PapamonMasterApp Master"
    sudo systemctl status papamonMasterApp.service
else
    echo "Uso: $0 [papamon|master]"
fi
