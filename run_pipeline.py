import pandas as pd
from pathlib import Path
from data_pipeline.log_manager import setup_logging
from data_pipeline.data_export import export_to_json
from data_pipeline.data_loading import load_csv, load_json
from data_pipeline.data_processing import clean_data, find_drug_mentions, build_drug_mention_graph
from data_pipeline.ad_hoc_functions import journal_with_most_unique_drugs, find_related_drugs
    
def run_pipeline(
    path_drugs_csv: str = 'input_data/drugs.csv',
    path_pubmed_csv: str = 'input_data/pubmed.csv',
    path_pubmed_json: str = 'input_data/pubmed.json',
    path_clinical_trials_csv: str = 'input_data/clinical_trials.csv',
    drug_mentions_path: str = 'output_data/drug_mentions_graph.json'
) -> None:
    """
    Run medical data pipeline process: load, clean, process data to build drug-mention graph. 
    Perform ad-hoc treatment:
    - find journal with max number of different drugs; 
    - find all drugs in journals, from journals where defined drug was mentioned (exclude Clinical Trials).
    """
    # Convert all paths to Path objects
    drug_mentions_path = Path(drug_mentions_path)
    path_drugs_csv = Path(path_drugs_csv)
    path_pubmed_csv = Path(path_pubmed_csv)
    path_pubmed_json = Path(path_pubmed_json)
    path_clinical_trials_csv = Path(path_clinical_trials_csv)
    
    # Load data
    drugs_df = load_csv(path_drugs_csv)
    pubmed_csv_df = load_csv(path_pubmed_csv)
    pubmed_json_df = load_json(path_pubmed_json)
    clinical_trials_df = load_csv(path_clinical_trials_csv)

    # Clean data
    drugs_df = clean_data(drugs_df)
    pubmed_csv_df = clean_data(pubmed_csv_df)
    pubmed_json_df = clean_data(pubmed_json_df)
    clinical_trials_df = clean_data(clinical_trials_df)

    # Process data
    mentions_csv_df = find_drug_mentions(drugs_df, pubmed_csv_df, 'title', 'pubmed')
    mentions_json_df = find_drug_mentions(drugs_df, pubmed_json_df, 'title', 'pubmed')
    mentions_trials_df = find_drug_mentions(drugs_df, clinical_trials_df, 'scientific_title', 'clinical_trials')

    # Concatenate processed data
    all_mentions = pd.concat([mentions_csv_df, mentions_json_df, mentions_trials_df], ignore_index=True)

    # Group journals by drug
    drug_mentions_graph = build_drug_mention_graph(all_mentions)

    # Export results
    export_to_json(drug_mentions_graph, drug_mentions_path)
    
    # Ad-hoc treatment
    # Print the name of the journal that mentions the most different drugs
    journal_name, unique_drug_count = journal_with_most_unique_drugs(drug_mentions_graph)
    print(f"The journal with the most unique drug mentions is: {journal_name} with {unique_drug_count} drugs.")
    
    # Find all drugs mentioned in the same journals as the target drug in pubmed
    related_drugs = find_related_drugs(drug_mentions_graph, 'BETAMETHASONE', 'pubmed')
    print(f"Drugs mentioned in the same PubMed journals as BETAMETHASONE: {related_drugs}")
    
if __name__ == "__main__":
    setup_logging()
    run_pipeline()
    
    while True:
        user_input = input("\nPress Enter to exit or type 'r' and press Enter to relaunch: ").strip().lower()
        
        if user_input == 'r':
            print("\nRelaunching the script...\n")
            run_pipeline() 
        elif user_input == '':
            print("Exiting.")
            break
        else:
            print("Invalid input. Press Enter to exit or type 'r' and press Enter to relaunch.")
