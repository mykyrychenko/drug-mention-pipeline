import os
import json
import unittest
from run_pipeline import run_pipeline

class TestFullPipeline(unittest.TestCase):
    
    def setUp(self):
        """
        Set up test paths for input, output, and reference data.
        """
        self.input_folder = 'tests/test_data/input_data/'
        self.output_file = 'tests/test_data/output_data/drug_mentions.json'
        self.reference_file = 'tests/test_data/reference_data/drug_mentions_reference.json'
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

    def test_full_pipeline(self):
        """
        Run the full pipeline and compare the output with the reference.
        """
        # Run the pipeline using the files in `input_folder` and save output to `output_file`
        run_pipeline(
            path_drugs_csv=f"{self.input_folder}/drugs.csv",
            path_pubmed_csv=f"{self.input_folder}/pubmed.csv",
            path_pubmed_json=f"{self.input_folder}/pubmed.json",
            path_clinical_trials_csv=f"{self.input_folder}/clinical_trials.csv",
            drug_mentions_path=self.output_file
        )

        # Load generated output and reference data
        with open(self.output_file, 'r', encoding='utf-8') as f:
            generated_output = json.load(f)

        with open(self.reference_file, 'r', encoding='utf-8') as f:
            reference_output = json.load(f)

        # Assert that the generated output matches the reference output
        self.assertEqual(generated_output, reference_output)
            
if __name__ == '__main__':
    unittest.main()
