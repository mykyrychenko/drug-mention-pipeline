import logging 
from pathlib import Path

def setup_logging(path_log_file: str ='logs/data_pipeline.log') -> None:
    """
    Configure the logging system.
    """
    path_log_file = Path(path_log_file)
    # Create the directory log if it doesn't exist
    Path(path_log_file).parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.DEBUG,  # Set the base logging level
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(path_log_file),  # Log to a file
            logging.StreamHandler()  # Also output to terminal
        ]
    )