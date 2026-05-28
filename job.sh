#!/bin/bash

#SBATCH --job-name=astralog-hpc      ## Job name
#SBATCH --partition=g100_usr_prod    ## Standard partition for user jobs on Galileo100
#SBATCH --nodes=1                    ## Number of nodes
#SBATCH --ntasks=1                   ## Number of tasks (MPI processes)
#SBATCH --cpus-per-task=4            ## CPU cores per task
#SBATCH --time=00:10:00              ## Maximum execution time
#SBATCH --output=logs/%j_output.log  ## stdout → file (% j = job ID)
#SBATCH --error=logs/%j_error.log    ## stderr → file separato

module load profile/advanced
module load openmpi/4.1.1--gcc--10.2.0-cuda--11.1.0
module load singularity/3.8.0--bind--openmpi--4.1.1  ## Load Singularity on Galileo100

SIF_PATH=$HOME/astralog.sif  ## .sif container path
INPUT_DIR=$(pwd)/input        ## Input directory path
OUTPUT_DIR=$(pwd)/results     ## Output directory path

mkdir -p logs                ## Create logs directory if it doesn't exist
mkdir -p $INPUT_DIR
mkdir -p $OUTPUT_DIR

singularity run \
    --bind $INPUT_DIR:/app/input \
    --bind $OUTPUT_DIR:/app/results \
    $SIF_PATH \
    --rules /app/input/rules.json \
    --input /app/input/telemetry_cleaned.csv \
    --output /app/results
