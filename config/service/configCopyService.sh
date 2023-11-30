#!/bin/bash
# Script que copia el servicio en systemd
# Autor: Agustin Giannoni

# Verifica si se proporcionaron los dos parámetros necesarios
if [ $# -ne 2 ]; then
    echo "Por favor, proporciona la ruta al archivo de servicio y la ruta de destino."
    echo "Ejemplo: $0 /ruta/al/archivo/servicio.service /ruta/de/destino/"
    exit 1
fi

# Ruta al archivo de servicio proporcionada como primer parámetro
archivo_servicio="$1"

# Ruta de destino proporcionada como segundo parámetro
ruta_destino="$2"

# Verifica si el archivo de servicio existe
if [ ! -f "$archivo_servicio" ]; then
    echo "El archivo de servicio no existe en la ubicación especificada."
    exit 1
fi

# Copia el archivo de servicio a la ruta de destino con permisos sudo
sudo cp -f "$archivo_servicio" "$ruta_destino"

# Verifica el estado de la copia
if [ $? -eq 0 ]; then
    echo "El archivo de servicio se copió correctamente a $ruta_destino."
else
    echo "Hubo un problema al copiar el archivo de servicio."
fi
