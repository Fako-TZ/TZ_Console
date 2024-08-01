import os
import sys
import time
import json
import traceback
from datetime import datetime
from typing import Optional, Callable, Any, Union, Dict

# ANSI color codes for text formatting
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Symbols for different message types
class Symbols:
    INFO = '[INFO]'
    WARNING = '[WARN]'
    ERROR = '[ERROR]'
    DEBUG = '[DEBUG]'
    CUSTOM = '[CUSTOM]'
    SUCCESS = '[SUCCESS]'
    FAILURE = '[FAILURE]'
    CRITICAL = '[CRITICAL]'

# Default configuration
DEFAULT_CONFIG = {
    'log_levels': {
        Symbols.INFO: True,
        Symbols.WARNING: True,
        Symbols.ERROR: True,
        Symbols.DEBUG: False,
        Symbols.SUCCESS: True,
        Symbols.FAILURE: True,
        Symbols.CRITICAL: True
    },
    'log_file': 'log.txt',
    'log_rotation': True,
    'log_rotation_size': 10485760  # 10 MB
}

def load_config(config_path: str) -> Dict[str, Any]:
    """Loads configuration from a specified path."""
    try:
        with open(config_path, 'r') as config_file:
            config = json.load(config_file)
            log_success("Configuration loaded successfully.")
            return config
    except Exception as e:
        log_error(f"Error loading configuration: {e}")
        return DEFAULT_CONFIG

def rotate_log_file(file_path: str) -> None:
    """Rotates the log file."""
    if os.path.exists(file_path):
        base, ext = os.path.splitext(file_path)
        for i in reversed(range(5)):
            old_file = f"{base}.{i+1}{ext}"
            new_file = f"{base}.{i}{ext}"
            if os.path.exists(old_file):
                os.rename(old_file, new_file)
        os.rename(file_path, f"{base}.1{ext}")

def get_timestamp() -> str:
    """Returns the current timestamp in a readable format."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_message(
    message: str,
    level: str = Symbols.INFO,
    color: str = Colors.WHITE,
    to_file: bool = False,
    config: Optional[Dict[str, Any]] = None,
    console: bool = True,
    end: str = '\n'
) -> None:
    """Logs a message with a specific symbol and color, optionally to a file and/or console."""
    if config is None:
        config = DEFAULT_CONFIG

    if not config['log_levels'].get(level, True):
        return

    formatted_message = f"{color}{level} {get_timestamp()} - {message}{Colors.RESET}"
    if console:
        print(formatted_message, end=end)

    if to_file:
        file_path = config.get('log_file', 'log.txt')
        if config.get('log_rotation', True):
            log_file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
            if log_file_size >= config.get('log_rotation_size', 10485760):  # Default 10 MB
                rotate_log_file(file_path)

        with open(file_path, 'a') as log_file:
            log_file.write(f"{level} {get_timestamp()} - {message}\n")

def clear_terminal() -> None:
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')
    log_message("Terminal cleared", level=Symbols.INFO, color=Colors.GREEN)

# Specific log functions
def log_info(message: str, to_file: bool = False, config: Optional[Dict[str, Any]] = None) -> None:
    log_message(message, level=Symbols.INFO, color=Colors.CYAN, to_file=to_file, config=config)

def log_warning(message: str, to_file: bool = False, config: Optional[Dict[str, Any]] = None) -> None:
    log_message(message, level=Symbols.WARNING, color=Colors.YELLOW, to_file=to_file, config=config)

def log_error(message: str, to_file: bool = False, config: Optional[Dict[str, Any]] = None) -> None:
    log_message(message, level=Symbols.ERROR, color=Colors.RED, to_file=to_file, config=config)

def log_debug(message: str, to_file: bool = False, config: Optional[Dict[str, Any]] = None) -> None:
    log_message(message, level=Symbols.DEBUG, color=Colors.MAGENTA, to_file=to_file, config=config)

def log_success(message: str, to_file: bool = False, config: Optional[Dict[str, Any]] = None) -> None:
    log_message(message, level=Symbols.SUCCESS, color=Colors.GREEN, to_file=to_file, config=config)

def log_failure(message: str, to_file: bool = False, config: Optional[Dict[str, Any]] = None) -> None:
    log_message(message, level=Symbols.FAILURE, color=Colors.RED, to_file=to_file, config=config)

def log_critical(message: str, to_file: bool = False, config: Optional[Dict[str, Any]] = None) -> None:
    log_message(message, level=Symbols.CRITICAL, color=Colors.BOLD + Colors.RED, to_file=to_file, config=config)

def log_custom(message: str, symbol: str = Symbols.CUSTOM, color: str = Colors.BLUE, to_file: bool = False, config: Optional[Dict[str, Any]] = None) -> None:
    log_message(message, level=symbol, color=color, to_file=to_file, config=config)

def handle_exception(exc_type, exc_value, exc_traceback, config: Optional[Dict[str, Any]] = None) -> None:
    """Handles exceptions by logging the traceback."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    log_error(f"Uncaught exception: {exc_value}", config=config)
    formatted_traceback = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
    log_message(formatted_traceback, level=Symbols.ERROR, color=Colors.RED, to_file=True, config=config)

sys.excepthook = lambda exc_type, exc_value, exc_traceback: handle_exception(exc_type, exc_value, exc_traceback, load_config("TZ_CustomConsole/config.json"))

def time_function(func: Callable) -> Callable:
    """Decorator to measure the execution time of a function."""
    def wrapper(*args, **kwargs) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        log_debug(f"Function '{func.__name__}' executed in {end_time - start_time:.4f} seconds.")
        return result
    return wrapper

def print_progress_bar(iteration: int, total: int, prefix: str = '', suffix: str = '', length: int = 50, fill: str = '█', print_end: str = "\r") -> None:
    """Prints a progress bar to the terminal."""
    percent = f"{100 * (iteration / float(total)):.1f}"
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    if iteration == total:
        print()