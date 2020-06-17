import os
import sys

sys.path.append("../src")

# Define constants.
data_dir = "/beegfs/vl1019/drucker2020naoc_data"
in_dir = os.path.join(data_dir, "BOGOTA_NFCs_2018")
swift_names = os.listdir(in_dir)
script_name = os.path.basename(__file__)
script_path = os.path.join("..", "src", script_name)


# Create folder.
sbatch_dir = os.path.join(script_name[:-3], "sbatch")
os.makedirs(sbatch_dir, exist_ok=True)
slurm_dir = os.path.join(script_name[:-3], "slurm")
os.makedirs(slurm_dir, exist_ok=True)


# Loop over recording units.
for swift_name in swift_names:
    date_str = os.path.split(swift_name)[1]
    script_path_with_args = " ".join([script_path, date_str])
    job_name = "_".join([script_name.split("_")[0], date_str])
    file_name = job_name + ".sbatch"
    file_path = os.path.join(sbatch_dir, file_name)

    # Geneate file.
    with open(file_path, "w") as f:
        f.write("#!/bin/bash\n")
        f.write("\n")
        f.write("#BATCH --job-name=" + script_name.split("_")[0] + "\n")
        f.write("#SBATCH --nodes=1\n")
        f.write("#SBATCH --tasks-per-node=1\n")
        f.write("#SBATCH --cpus-per-task=1\n")
        f.write("#SBATCH --time=6:00:00\n")
        f.write("#SBATCH --mem=8GB\n")
        f.write("#SBATCH --output=../slurm/" + job_name + "_%j.out\n")
        f.write("\n")
        f.write("module purge\n")
        f.write("source activate bvp")
        f.write("\n")
        f.write("# The first argument is the date of the recording.\n")
        f.write("python " + script_path_with_args)


# Open shell file.
file_name = "_".join([script_name.split("_")[0]])
file_path = os.path.join(sbatch_dir, file_name + ".sh")
with open(file_path, "w") as f:

    # Loop over recording units.
    for swift_name in sorted(swift_names):
        date_str = os.path.split(swift_name)[1]
        job_name = "_".join([script_name.split("_")[0], date_str])
        sbatch_str = "sbatch " + job_name + ".sbatch"

        # Write SBATCH command to shell file.
        f.write(sbatch_str + "\n")

# Grant permission to execute the shell file.
# https://stackoverflow.com/a/30463972
mode = os.stat(file_path).st_mode
mode |= (mode & 0o444) >> 2
os.chmod(file_path, mode)
