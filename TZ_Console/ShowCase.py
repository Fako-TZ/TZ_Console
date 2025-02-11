import os
import time
import json
from typing import Optional, Dict
from TZ_CustomConsole.TZ_terminal_utils import *

def print_menu() -> None:
    
    # Prints the main menu.
    clear_terminal()
    print("==== TZ Console Application Menu ====")
    print("1. Demonstrate logging at different levels")
    print("2. Show progress bar")
    print("3. Display configuration")
    print("4. Exit")
    print("===================================")

def main() -> None:
    config = load_config()
    
    while True:
        print_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == '1':
            clear_terminal()
            print("==== Logging Demonstrations ====")
            log_info("This is an informational message.", config)
            log_warning("This is a warning message.", config)
            log_error("An error occurred during processing.", config)
            log_debug("Debugging information.", config)
            log_success("Operation completed successfully.", config)
            log_failure("Operation failed to complete.", config)
            log_critical("Critical error encountered.", config)
            log_custom("This is a custom message with a custom symbol and color.", "[MYAPP]", Colors.MAGENTA, config)
            input("Press Enter to return to the menu...")

        elif choice == '2':
            clear_terminal()
            print("==== Progress Bar Demonstration ====")
            total_items = 10
            for i in range(total_items):
                time.sleep(0.5)
                print_progress_bar(i + 1, total_items, 'Progress:', 'Complete', 50)
            input("Press Enter to return to the menu...")

        elif choice == '3':
            clear_terminal()
            print("==== Display Configuration ====")
            print(json.dumps(config, indent=4))
            input("Press Enter to return to the menu...")

        elif choice == '4':
            clear_terminal()
            print("Exiting the application. Goodbye!")
            break

        elif choice == '5':
            print(os.getcwd())
            input("Press Enter to return to the menu...")

        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
            time.sleep(1)

if __name__ == "__main__":
    main()