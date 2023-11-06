#!/bin/bash

if [ "$1" == "slave" ]; then
    echo "Configurando el servicio PapamonApp Slave"
    sudo systemctl enable papamonApp.service
    sudo systemctl disable papamonMasterApp.service
    sudo systemctl daemon-reload
    sudo systemctl start papamonApp.service
elif [ "$1" == "master" ]; then
    echo "Configurando el servicio PapamonMasterApp Master.."
    sudo systemctl enable papamonMasterApp.service
    sudo systemctl disable papamonApp.service
    sudo systemctl daemon-reload
    sudo systemctl start papamonMasterApp.service
else
    echo "Uso: $0 [papamon|master]"
fi
