import subprocess
import time
import sys

# ANSI escape codes for colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

def run_command(command, task_description=""):
    """
    Runs a shell command and provides real-time output and error handling.
    """
    print(f"\n{BLUE}{BOLD}--> Executing: {task_description if task_description else command}{RESET}")
    try:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, shell=True, bufsize=1)

        # Print stdout in real-time
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()

        process.wait()

        if process.returncode != 0:
            error_output = process.stderr.read()
            print(f"{RED}{BOLD}Error during '{command}':{RESET}\n{error_output}")
            return False
        else:
            print(f"{GREEN}Command '{command}' completed successfully.{RESET}")
            return True
    except FileNotFoundError:
        print(f"{RED}Error: Command '{command.split()[0]}' not found. Is it installed and in your PATH?{RESET}")
        return False
    except Exception as e:
        print(f"{RED}An unexpected error occurred while running command: '{command}'\nDetails: {e}{RESET}")
        return False

def perform_system_maintenance(tasks):
    """
    Iterates through a list of tasks and runs each command.
    """
    print(f"\n{YELLOW}{BOLD}Starting system maintenance tasks...{RESET}")
    successful_tasks = 0

    for i, task in enumerate(tasks):
        command = task['command']
        description = task['description']
        
        print(f"\n{YELLOW}Task {i+1}/{len(tasks)}: {description}{RESET}")
        if run_command(command, description):
            successful_tasks += 1
        
        time.sleep(0.5) # Brief sleep for visual separation

    print(f"\n{GREEN}{BOLD}System maintenance complete!{RESET}")
    if successful_tasks == len(tasks):
        print(f"{GREEN}All {successful_tasks} tasks finished without errors. 🎉{RESET}")
    else:
        print(f"{YELLOW}Finished with {successful_tasks} out of {len(tasks)} tasks successful. Please review errors above. ⚠️{RESET}")

def main():
    """Main function to orchestrate the update and cleanup process."""
    print(f"{GREEN}{BOLD}--- UPDATE AND CLEAN YOUR SYSTEM ---{RESET}\n")

    maintenance_tasks = [
        {'command': "sudo apt update", 'description': "Updating package lists"},
        {'command': "sudo apt upgrade -y", 'description': "Upgrading installed packages"},
        {'command': "sudo apt autoremove -y", 'description': "Removing unused packages"},
        {'command': "sudo apt clean", 'description': "Cleaning up downloaded package files"},
        {'command': "sudo updatedb", 'description': "Updating the 'locate' database"}
    ]

    perform_system_maintenance(maintenance_tasks)

    print(f"\n{BLUE}Thank you for using this script!{RESET}")
    # Display @incredibit in alternating blue and green characters
    incredibit_text = "@incredibit"
    colored_incredibit = ""
    for i, char in enumerate(incredibit_text):
        if i % 2 == 0:
            colored_incredibit += BLUE + char
        else:
            colored_incredibit += GREEN + char
    print(colored_incredibit + RESET)

if __name__ == "__main__":
    main()
