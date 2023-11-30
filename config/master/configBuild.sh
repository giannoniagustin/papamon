#!/bin/bash
# Script para configurar build de PapamonApp Slave y PapamonApp Master
# Autor: Agustin Giannoni


# Verifica que se hayan proporcionado dos parámetros: directorio y nombre del Makefile
if [ $# -ne 2 ]; then
    echo "Por favor, proporciona el directorio que contiene los Makefiles y el nombre del Makefile."
    exit 1
fi

# Directorio que contiene los Makefiles proporcionado como primer parámetro
directorio_makefiles="$1"

# Nombre del Makefile proporcionado como segundo parámetro
makefile="$2"

# Verifica si el directorio existe
if [ ! -d "$directorio_makefiles" ]; then
    echo "El directorio especificado no existe."
    exit 1
fi

# Verifica si el Makefile existe en el directorio proporcionado
if [ ! -f "$directorio_makefiles/$makefile" ]; then
    echo "El Makefile especificado no existe en el directorio proporcionado."
    exit 1
fi
# Cambia al directorio donde se encuentra el Makefile
cd "$directorio_makefiles" || exit 1

# Ejecuta el comando make con el Makefile especificado
make -f "$directorio_makefiles/$makefile"
