import subprocess
import time
from tqdm import tqdm
import pyfiglet
import sys

# ANSI escape codes for colors
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BLUE = "\033[94m"
RESET = "\033[0m"
BOLD = "\033[1m"

# --- Function Definitions (should come before main) ---

def run_command(command, task_description=""):
    """
    Runs a shell command and provides real-time output and error handling.
    Args:
        command (str): The shell command to execute.
        task_description (str): A description of the task being performed, for better user feedback.
    Returns:
        bool: True if the command was successful, False otherwise.
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

def print_banner(large_text, small_text):
    """
    Prints large ASCII art text in green and small text in red, centered.
    """
    ascii_art = pyfiglet.figlet_format(large_text, font="slant")

    # Calculate padding for centering
    terminal_width = 80 # A common default, or you can try to get actual width
    lines = ascii_art.splitlines()
    max_line_length = max(len(line) for line in lines)

    centered_ascii_art = "\n".join([f"{' ' * ((terminal_width - max_line_length) // 2)}{line}" for line in lines])

    print(f"{GREEN}{BOLD}{centered_ascii_art}{RESET}")
    print(f"{RED}{' ' * ((terminal_width - len(small_text)) // 2)}{small_text}{RESET}\n")

def perform_system_maintenance(tasks):
    """
    Iterates through a list of tasks, runs each command, and updates a progress bar.
    Args:
        tasks (list): A list of dictionaries, each containing 'command' and 'description'.
    """
    print(f"\n{YELLOW}{BOLD}Starting system maintenance tasks...{RESET}")
    successful_tasks = 0

    with tqdm(total=len(tasks), desc=f"{GREEN}Overall Progress{RESET}", unit="task",
              bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}{postfix}]",
              colour="GREEN") as pbar:
        for i, task in enumerate(tasks):
            command = task['command']
            description = task['description']

            pbar.set_description(f"{YELLOW}Running: {description[:30]}{'...' if len(description) > 30 else ''}{RESET}") # Truncate description for progress bar

            if run_command(command, description):
                successful_tasks += 1
                pbar.set_postfix_str(f"Successful: {successful_tasks}/{len(tasks)}")
            else:
                pbar.set_postfix_str(f"Errors encountered!")
                # Optionally, break here or continue with other tasks

            pbar.update(1)
            time.sleep(0.5) # Brief sleep for visual separation

    print(f"\n{GREEN}{BOLD}System maintenance complete!{RESET}")
    if successful_tasks == len(tasks):
        print(f"{GREEN}All {successful_tasks} tasks finished without errors.{RESET}")
    else:
        print(f"{YELLOW}Finished with {successful_tasks} out of {len(tasks)} tasks successful. Please review errors above.{RESET}")

def main():
    """Main function to orchestrate the update and cleanup process."""
    print_banner("UNC", "Update and Clean Your System")

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
