from TZ_CustomConsole.TZ_terminal_utils import *


def main():
    config = load_config("TZ_CustomConsole/config.json")
    clear_terminal()
    log_info("Starting the application.", config=config)

    # Demonstrating logging at different levels
    log_info("This is an informational message.", config=config)
    log_warning("This is a warning message.", config=config)
    log_error("An error occurred during processing.", config=config)
    log_debug("Debugging information.", config=config)
    log_success("Operation completed successfully.", config=config)
    log_failure("Operation failed to complete.", config=config)
    log_critical("Critical error encountered.", config=config)

    # Demonstrating custom logging
    log_custom("This is a custom message with a custom symbol and color.", symbol="[MYAPP NAME HERE]", color=Colors.MAGENTA, config=config)

    # Demonstrating progress bar
    total_items = 10
    for i in range(total_items):
        time.sleep(0.1)
        print_progress_bar(i + 1, total_items, prefix='Progress:', suffix='Complete', length=50)

    # Demonstrating configuration loading
    log_info(f"Loaded configuration: {config}", config=config)

if __name__ == "__main__":
    main()
