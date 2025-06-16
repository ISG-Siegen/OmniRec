import subprocess
from pathlib import Path
from hpc_data_set_names import data_set_names
from settings import cluster_email

for data_set_name in data_set_names:
    paths_to_check = [Path(f"./data_sets/{data_set_name}/processed/interactions.csv"),
                      Path(f"./data_sets/{data_set_name}/processed/metadata.json"),
                      Path(f"./data_sets/{data_set_name}/processed/processing_log.txt")]
    skip = False
    for path_to_check in paths_to_check:
        if path_to_check.is_file() and path_to_check.stat().st_size > 0:
            skip = True
    if skip:
        continue
    script_name = f"__RSDL_Processing_{data_set_name}"
    script = "#!/bin/bash\n" \
             "#SBATCH --nodes=1\n" \
             "#SBATCH --cpus-per-task=1\n" \
             "#SBATCH --mail-type=FAIL\n" \
             f"#SBATCH --mail-user={cluster_email}\n" \
             "#SBATCH --partition=short,medium\n" \
             "#SBATCH --time=05:00:00\n" \
             "#SBATCH --mem=200G\n" \
             "#SBATCH --output=./omni_out/%x_%j.out\n" \
             "module load singularity\n" \
             "singularity exec --pwd /mnt --bind ./:/mnt ./data_loader.sif python -u " \
             f"./run_convert_raw_to_processed.py --data_set_name {data_set_name}"
    with open(f"./{script_name}.sh", 'w', newline='\n') as f:
        f.write(script)
    subprocess.run(["sbatch", f"./{script_name}.sh"])
    Path(f"./{script_name}.sh").unlink()
