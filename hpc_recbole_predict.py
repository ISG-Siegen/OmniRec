import subprocess
from pathlib import Path
from hpc_data_set_names import data_set_names
from hpc_algorithm_names import algorithm_names
from settings import cluster_email
from algorithm_config import retrieve_configurations

require_predictions_and_log = False

num_configurations = 0
for algorithm_name in algorithm_names:
    num_configurations += len(retrieve_configurations(algorithm_name=algorithm_name))
num_jobs = len(data_set_names) * num_configurations * 5
job_counter = 1

for data_set_name in data_set_names:
    for algorithm_name in algorithm_names:
        configurations = retrieve_configurations(algorithm_name=algorithm_name)
        for algorithm_config_index in range(len(configurations)):
            for fold in range(5):
                model_path = Path(
                    f"./data_sets/{data_set_name}/checkpoint_{algorithm_name}/"
                    f"config_{algorithm_config_index}/fold_{fold}/")
                model_path.mkdir(parents=True, exist_ok=True)
                exists = False
                if require_predictions_and_log:
                    predict_log = model_path.joinpath("predict_log.json")
                    predictions_file = model_path.joinpath("predictions.json")
                    if (predict_log.is_file() and predict_log.stat().st_size > 0 and
                            predictions_file.is_file() and predictions_file.stat().st_size > 0):
                        print(f"Predict log {predict_log.name} and predictions file {predictions_file.name} exist. "
                              f"Skipping job {job_counter}.")
                        exists = True
                    else:
                        print(f"Predict log file {predict_log.name} and/or "
                              f"predictions file {predictions_file.name} do not exist.")
                else:
                    for file in model_path.iterdir():
                        if ".out" in file.name and "RSDL_Recbole_Predict" in file.name:
                            if file.stat().st_size > 0:
                                print(f"HPC output file {file.name} exists. Skipping job {job_counter}.")
                                exists = True
                                break
                if not exists:

                    script = "#!/bin/bash\n" \
                             "#SBATCH --nodes=1\n" \
                             "#SBATCH --cpus-per-task=1\n" \
                             "#SBATCH --mail-type=FAIL\n" \
                             f"#SBATCH --mail-user={cluster_email}\n" \
                             "#SBATCH --partition=gpu\n" \
                             "#SBATCH --gres=gpu:1\n" \
                             "#SBATCH --time=00:32:00\n" \
                             "#SBATCH --mem=48G\n" \
                             f"#SBATCH --output={model_path}/%x_%j.out\n" \
                             "module load singularity\n" \
                             "singularity exec --nv --pwd /mnt --bind ./:/mnt ./data_loader.sif python -u " \
                             f"./run_recbole_predict.py --data_set_name {data_set_name} --algorithm_name {algorithm_name} " \
                             f"--algorithm_config {algorithm_config_index} --fold {fold}\n"
                    script_name = f"__RSDL_Recbole_Predict_{data_set_name}_{algorithm_name}_{fold}_{algorithm_config_index}.sh"
                    subprocess.run(["sbatch", "-J", script_name], input=script, universal_newlines=True)
                    print(f"Submitted job {job_counter}/{num_jobs}.")
                job_counter += 1
