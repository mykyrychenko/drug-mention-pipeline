from data_pipeline.data_loading import load_csv
from io import StringIO
import logging
import unittest
from data_pipeline.data_loading import load_csv, load_json
import pandas as pd


class TestDataLoading(unittest.TestCase):
    def test_load_csv(self):
        df = load_csv('input_data/clinical_trials.csv')
        self.assertIsInstance(df, pd.DataFrame)
        # Check that special characters are correctly loaded
        self.assertEqual(df.loc[4, 'journal'],"Hôpitaux Universitaires de Genève")
        self.assertIn("ñ", df.loc[4, 'scientific_title'])

    def test_load_json(self):
        df = load_json('input_data/pubmed.json')
        self.assertIsInstance(df, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
