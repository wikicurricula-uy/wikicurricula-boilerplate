import sys  # Import the sys module to access command-line arguments
import multiprocessing #for parallel execution of subprocesses.
import subprocess  # for running external shell commands.

# Check if the language code is provided as a command-line argument
if len(sys.argv) > 1:
    WIKIPEDIA_LANGUAGE  = sys.argv[1]
else:
    WIKIPEDIA_LANGUAGE = "en"  # Default to "en" if no argument is provided

# or exit the process
# if len(sys.argv) < 2:
#     print("Please provide the language code as a command-line argument (e.g., 'en' for English).")
#     sys.exit(1)

def run_subprocess(command):
    # Function to run a subprocess
    subprocess.run(command, shell=True)

if __name__ == "__main__":
    # List of commands to run in parallel
    commands = [
        f"python query.py {WIKIPEDIA_LANGUAGE}",
        f"python bot.py {WIKIPEDIA_LANGUAGE}",
        "python translate.py",
    ]

    # creates a multiprocessing pool with a specified number of processes (in this case, 3).
    num_processes = 3
    pool = multiprocessing.Pool(processes=num_processes)
    pool.map(run_subprocess, commands)      # Use the pool to run the commands concurrently

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

    print("All subprocesses have completed.")










