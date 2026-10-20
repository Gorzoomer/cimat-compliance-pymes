#!/bin/bash
# ==============================================================================
# Script de Slurm para el Laboratorio de Supercómputo del CIMAT (Frente 4)
# Proyecto: Evaluación Exploratoria de Compliance (ISO 37301) y Redes 69-B
# Cuenta autorizada: proy_ai26_manuel.ledesma (Dr. Manuel Ledesma López)
# Subequipo de Arquitectura: Luis Alonzo Hernández Silva, Santiago Aguilar H.
# ==============================================================================

# Partición de cómputo en CPU (C1Mitad1 = 12 núcleos/nodo; C2 = 24 núcleos/nodo)
#SBATCH --partition=C1Mitad1

# Nombre identificativo del trabajo en la cola de Slurm (squeue)
#SBATCH --job-name=cimat_pymes_69b

# Número de tareas y núcleos solicitados (ajustado a un nodo de C1Mitad1)
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=12

# Archivo de bitácora del manejador Slurm (nuestro software en Python escribe
# directamente a disco en data/processed/ sin imprimir a stdout, conforme a la
# página 18 del Manual de Acceso a Recursos del CIMAT)
#SBATCH --output=slurm_cimat_job.log

# Memoria máxima por nodo (0 = acceso a la memoria disponible del nodo asignado)
#SBATCH --mem=0

# Límite de tiempo de ejecución para prevenir procesos colgados (01:00:00 = 1 hora)
#SBATCH --time=01:00:00

export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

# Ejecución secuencial de los módulos reproducibles (escriben directo a archivo)
python3 -m src.homologacion
python3 -m src.graph_builder
