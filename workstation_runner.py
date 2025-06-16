import argparse
import asyncio
import sys
from hpc_data_set_names import data_set_names
from hpc_algorithm_names import algorithm_names
from recbole_algorithm_config import retrieve_configurations


async def parallel_process(i, semaphore):
    async with semaphore:
        process = await asyncio.create_subprocess_exec(*processes[i])
        await process.wait()


async def run_worker(parallel_processes):
    sem = asyncio.Semaphore(parallel_processes)
    await asyncio.gather(*[parallel_process(i, sem) for i in range(len(processes))])


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Workstation Runner Fit RecBole")
    parser.add_argument('--mode', dest='mode', type=str, required=True)
    parser.add_argument('--parallel_processes', dest='parallel_processes', type=int, required=True)
    args = parser.parse_args()

    if args.mode not in ["fit", "predict", "evaluate"]:
        raise ValueError("Invalid mode. Use 'fit', 'predict' or 'evaluate'.")

    processes = []
    for data_set_name in data_set_names:
        for algorithm_name in algorithm_names:
            configurations = retrieve_configurations(algorithm_name=algorithm_name)
            for algorithm_config_index in range(len(configurations)):
                for fold in range(5):
                    processes.append(
                        [sys.executable, f"./run_recbole_{args.mode}.py", "--data_set_name", data_set_name, "--algorithm_name",
                         algorithm_name, "--algorithm_config", str(algorithm_config_index), "--fold", str(fold)])

    asyncio.run(run_worker(args.parallel_processes))
