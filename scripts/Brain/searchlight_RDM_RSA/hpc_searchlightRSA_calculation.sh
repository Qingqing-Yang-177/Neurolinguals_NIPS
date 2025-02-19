#!/bin/bash
#
#SBATCH --job-name=searchlighRSA-Cal_Job
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=10
#SBATCH --mem=80GB
#SBATCH --time=48:00:00
#SBATCH --mail-type=END
#SBATCH --mail-user=qy775@nyu.edu
#SBATCH --output=/scratch/qy775/nma/slurm_out/slurm%j.out

# Activate the virtual environment
source /scratch/qy775/nma/nmaenv/bin/activate

# Set the PyTorch CUDA memory configuration
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

# module load python/3.11 skipped since the virtual env has python already
module load cuda/11.1.74

set -x
llm_label=$1 #eg. rdm_codellama_last, rdm_codellama, rdm_llama_last, rdm_llama, RDM_CogVLM2_last, RDM_CogVLM2_mid

python /scratch/qy775/nma/searchlightRSA_calculation.py "$llm_label" 

exit # tell python to exit
