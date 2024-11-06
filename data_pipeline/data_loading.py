import re
import io
import json
import logging
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

def load_csv(file_path: Path) -> pd.DataFrame:
    """
    Load a CSV file into a pandas DataFrame.
    """
    try:       
        logging.info(f"Loading CSV file from {file_path}")
        # Handling potential escape sequences and encoding issues
        with open(file_path, 'r', encoding='unicode_escape') as f:
            content = f.read()
            content = content.encode('raw_unicode_escape').decode('utf-8', errors='ignore')
                
        # Use io.StringIO to create a file-like object for pandas to read
        csv_data = io.StringIO(content)
        # Load into DataFrame
        return pd.read_csv(csv_data)
    
    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}")
        raise e

def remove_trailing_commas_json(json_str: str) -> str:
    """
    Removes trailing commas in string.
    """
    # Use regex to find and remove trailing commas before closing brackets/parentheses
    cleaned_json_str = re.sub(r',(\s*[\]}])', r'\1', json_str)
    return cleaned_json_str

def load_json(file_path: Path) -> pd.DataFrame:
    """
    Load a JSON file into a pandas DataFrame.
    """
    try:
        logging.info(f"Loading JSON file from {file_path}")
        with open(file_path, 'r', encoding='unicode_escape') as f:
            content = f.read()
            # Remove trailing commas before decoding the JSON
            content = remove_trailing_commas_json(content)
            # Handling potential escape sequences and encoding issues
            content = content.encode('raw_unicode_escape').decode('utf-8', errors='ignore')
            data = json.loads(content)
        return pd.DataFrame(data)

    except FileNotFoundError as e:
        logging.error(f"File not found: {file_path}")
        raise e
    except json.JSONDecodeError as e:
        logging.error(f"Skipping JSON file: {file_path}")
        raise e
