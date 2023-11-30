#!/bin/bash
directorio="/home/papamon/Documents/papamon"
rama="realease"
directorio_service="/home/papamon/Documents/papamon/config/service"  # Ruta al repositorio donde se encuentra el archivo del servicio
archivo_servicio="papamonApp.service"  # Nombre del archivo de servicio
directorio_systemd="/etc/systemd/system"  # Carpeta de systemd donde deseas copiar el archivo
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
echo "Configurando el servicio PapamonApp Slave"
echo "Forzando git pull en $directorio y rama $rama"
cd "$directorio"
git fetch --all
git reset --hard "origin/$rama"  # Utilizar la variable para la rama
git pull "origin/$rama" --force  # Utilizar la variable para la rama en el pull

echo "Compilando el proyecto"
make /home/papamon/Documents/papamon/reconstruct/Makefile

if  has_start_param  "$@" ; then
    echo "Configurando Inicio de servicio PapamonApp Slave"

    # Copiar el archivo del servicio a la carpeta de systemd y reemplazarlo si ya existe
    echo "Copiando el archivo de servicio $archivo_servicio a $directorio_systemd"
    sudo cp -f "$directorio_repositorio/$archivo_servicio" "$directorio_systemd/"
        
    sudo systemctl daemon-reload
    sudo systemctl stop $archivo_servicio
    sudo systemctl enable $archivo_servicio
    sudo systemctl start  $archivo_servicio
    sudo systemctl status $archivo_servicio
elif has_stop_param  "$@"; then
    echo "Configurando Detencion de servicio PapamonApp Slave"
    sudo systemctl stop $archivo_servicio
    sudo systemctl disable $archivo_servicio
    sudo systemctl status $archivo_servicio
fi

