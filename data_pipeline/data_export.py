import os
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def export_to_json(data: dict, output_file: Path) -> None:
    """
    Export data to a JSON file.
    """

    # Ensure the directory exists
    output_dir = os.path.dirname(output_file)
    if os.path.isdir(output_dir) and not os.path.exists(output_dir):
        logging.info(f"Creating output directory: {output_dir}")
        os.makedirs(output_dir)

    # Write the JSON data to the file
    logging.info(f"Exporting data to JSON file {output_file}")
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4)
