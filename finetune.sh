#!/bin/bash
#SBATCH --account=e32706     # Replace with your actual Quest allocation account
#SBATCH --partition=gengpu # Replace with your desired partition (e.g., gpu)
#SBATCH --gres=gpu:1                 # Request 1 GPU (adjust type if needed, e.g., gpu:a100:1)
#SBATCH --time=48:00:00              # Set a reasonable time limit (HH:MM:SS)
#SBATCH --mem=64G                    # Memory per node (adjust based on dataset/model size, 32G is a common value for GPU jobs)
#SBATCH --nodes=1                    # Number of nodes
#SBATCH --job-name=GPT2_Finetuning   # Job name
#SBATCH --ntasks=1                   # Number of tasks (usually 1 for single GPU)
#SBATCH --cpus-per-task=8            # Number of CPU cores per task (matching example)
#SBATCH --mail-type=ALL              # Email notifications for job events
#SBATCH --mail-user=ashleshaahirwadi2025@u.northwestern.edu     # Replace with your email address

# Project configuration
PROJECT_NAME="GPT2_Finetuning_Run1"       # Name for this specific run
# Assuming logs directory within GENAI_2, adjust if needed
LOGS_DIR="/home/ccx4276/GENAI_2/logs/"
PROJECT_RUN_DIR="${LOGS_DIR}/${PROJECT_NAME}"
mkdir -p ${PROJECT_RUN_DIR}

# Environment setup
module purge
# Load CUDA and cuDNN first
# module load cuda/11.8  # Or the appropriate CUDA version
# module load cudnn/8.6.0  # Or the appropriate cuDNN version
# Then source and activate conda
source /home/ccx4276/miniconda/etc/profile.d/conda.sh
conda activate deno                       # Replace with the name of your conda environment
# You might still need to load the python module here if your conda env doesn't handle it
module load python/anaconda3.10

# Performance settings (matching example)
export OMP_NUM_THREADS=8
export MKL_NUM_THREADS=8
export CUDA_CACHE_DISABLE=0
export CUDA_AUTO_BOOST=1

# Navigate to your project directory (assuming finetune_gpt2.py is here)
cd /home/ccx4276/GENAI_2 # Adjust path if necessary

# Export runtime directory variable (adapting from example)
export GPT2_RUN_DIR=${PROJECT_RUN_DIR}
echo "Exported GPT2_RUN_DIR=${GPT2_RUN_DIR}"

# Training command
echo "Starting GPT-2 finetuning..."
# Assuming writing_prompts.txt is in the current directory, or provide full path
# Output model will be saved inside the project run directory
python3 finetune_gpt2.py \
  --train_file "writing_prompts.txt" \
  --output_dir "${PROJECT_RUN_DIR}/finetuned_model" \
  --epochs 5 # Adjust number of epochs as needed

# Redirect standard output and error to log files within the run directory
> ${PROJECT_RUN_DIR}/output.log 2> ${PROJECT_RUN_DIR}/error.log

echo "Finetuning completed!"