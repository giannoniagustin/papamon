#!/bin/bash
# Script para configurar build de PapamonApp Slave y PapamonApp Master
# Autor: Agustin Giannoni
# Ejemplo de uso: sudo ./configAllBuild.sh


# Llama al script script_make.sh con parámetros fijos
ruta_makefiles="/home/papamon/Documents/papamon/reconstruct"  # Reemplaza con la ubicación real
nombre_makefile="Makefile"  # Reemplaza con el nombre real
nombre_makefile_reconstruct="Makefile_reconstruct"  # Reemplaza con el nombre real


# Llama al script script_make.sh con los parámetros fijos
./configBuild.sh "$ruta_makefiles" "$nombre_makefile"

# Llama al script script_make.sh con los parámetros fijos
./configBuild.sh "$ruta_makefiles" "$nombre_makefile_reconstruct"
