import subprocess
from pathlib import Path
from settings import cluster_email

script_name = f"__RSDL_Clear"
script = "#!/bin/bash\n" \
         "#SBATCH --nodes=1\n" \
         "#SBATCH --cpus-per-task=1\n" \
         "#SBATCH --mail-type=FAIL\n" \
         f"#SBATCH --mail-user={cluster_email}\n" \
         "#SBATCH --partition=short,medium,long\n" \
         "#SBATCH --time=00:30:00\n" \
         "#SBATCH --mem=16G\n" \
         "#SBATCH --output=./omni_out/%x_%j.out\n" \
         "module load singularity\n" \
         "singularity exec --pwd /mnt --bind ./:/mnt ./data_loader.sif python -u " \
         "./run_clear_data.py --data_origin processed --safety_flag True"
with open(f"./{script_name}.sh", 'w', newline='\n') as f:
    f.write(script)
subprocess.run(["sbatch", f"./{script_name}.sh"])
Path(f"./{script_name}.sh").unlink()
