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
        "python extract_article_name.py query_result.csv",
        f"python bot.py {WIKIPEDIA_LANGUAGE}",
        "python translate.py",
    ]

    # creates a multiprocessing pool with a specified number of processes (in this case, 4).
    num_processes = 4  
    pool = multiprocessing.Pool(processes=num_processes)

    # Use the pool to run the commands concurrently
    pool.map(run_subprocess, commands)

    # Close the pool and wait for all processes to finish
    pool.close()
    pool.join()

    print("All subprocesses have completed.")




















# Check if the language code is provided as a command-line argument
# if len(sys.argv) > 1:
#     WIKIPEDIA_LANGUAGE  = sys.argv[1]
# else:
#     WIKIPEDIA_LANGUAGE = "en"  # Default to "en" if no argument is provided

# # or exit the process
# # if len(sys.argv) < 2:
# #     print("Please provide the language code as a command-line argument (e.g., 'en' for English).")
# #     sys.exit(1)


# # Define the paths to the external scripts (bot1.py, bot2.py, bot3.py)
# scripts = ["query.py", "extract.py", "bot.py", "translate.py"]


# processes = [] # Initialize a list to store the subprocess objects

# try:
#     # Start each subprocess and store the process object
#     for script in scripts:
#         process = subprocess.Popen(["python", script, WIKIPEDIA_LANGUAGE])
#         processes.append(process)

#     # Wait for all subprocesses to complete
#     for process in processes:
#         process.wait()

#     print("All subprocesses have completed.")

# except subprocess.CalledProcessError as e:
#     print(f"Error running a subprocess: {e}")
# except FileNotFoundError as e:
#     print(f"External script not found: {e.filename}")
# except Exception as e:
#     print(f"An unexpected error occurred: {str(e)}")

