# SLURM Integration

If you want to use a HPC cluster with SLURM to run your experiments, you can leverage the built-in SLURM integration of the framework. This allows you to distribute the execution of different algorithm configurations across multiple compute nodes managed by SLURM.

## Enabling SLURM Integration

To enable SLURM integration, pass the path to a SLURM script to the [`run_omnirec()`](API_references.md#omnirec.util.run.run_omnirec) function using the `slurm_script` parameter:

```python
from omnirec.util.run import run_omnirec

# Define SLURM configuration
slurm_script = "path/to/slurm_script.slurm"

# Run experiments with SLURM integration
run_omnirec(
    datasets=dataset,
    plan=plan,
    evaluator=evaluator,
    slurm_script=slurm_script
)
```

## SLURM Script Template

The SLURM script defines the resource requirements and execution environment for each job. Here's a template:

```bash
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --cpus-per-task=1
#SBATCH --partition=medium
#SBATCH --output=${log_path}/%x_%j.out
#SBATCH --error=${log_path}/%x_%j.out
#SBATCH --job-name=${job_name}

${runner}
```

## Template Variables

The framework provides several variables that are automatically replaced when submitting jobs:

**`${runner}`** ✅ *Required*

- The command to execute the OmniRec runner for a specific algorithm configuration
- Automatically filled by the framework
- **Must** be included in your script

**`${log_path}`** ⬜ *Optional*

- Path where log files should be stored
- Useful for organizing SLURM output and error logs

**`${job_name}`** ⬜ *Optional*

- Name of the SLURM job
- Typically reflects the algorithm and configuration being run

Configure other SLURM directives (e.g., `--nodes`, `--cpus-per-task`, `--partition`, `--mem`) based on your cluster configuration and experiment requirements.

## How It Works

When you run [`run_omnirec()`](API_references.md#omnirec.util.run.run_omnirec) with the `slurm_script` parameter, the framework will:

1. Generate a separate SLURM job for each algorithm configuration in your [`ExperimentPlan`](API_references.md#omnirec.runner.plan.ExperimentPlan)
2. Replace template variables (`${runner}`, `${log_path}`, `${job_name}`) with appropriate values
3. Submit each job to the SLURM scheduler using `sbatch`
4. Allow distributed execution across your HPC cluster's compute nodes

This enables efficient parallel execution of multiple algorithm configurations, significantly reducing total experiment time on HPC clusters.