import logging
import pandas as pd

logger = logging.getLogger(__name__)

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean the DataFrame by handling missing values and mixed date formats.
    """
    if df.empty:
        logging.warning("DataFrame is empty.")
        return df

    # Cast all 'id' to the same format: str
    if 'id' in df.columns:
        df['id'] = df['id'].astype(str)

    # Handle mixed date formats
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'], format='mixed').dt.strftime('%d-%m-%Y')

    # Drop duplicates
    df = df.drop_duplicates()
    
    # Convert NaN values to None
    df = df.where(pd.notnull(df), None)
    
    # Replace empty strings with None
    df = df.replace('', None)

    return df

def find_drug_mentions(drugs_df: pd.DataFrame, publications_df: pd.DataFrame, title_col: str, publication_type: str) -> pd.DataFrame:
    """
    Find mentions of drugs in publication titles.
    """

    # Convert drug names and titles to lowercase
    drugs_df['drug_lower'] = drugs_df['drug'].str.lower()
    publications_df['title_lower'] = publications_df[title_col].str.lower()

    # Cross-join between the drugs_df and publications_df
    drugs_df['key'] = 1  # Temporary key column for cross join
    publications_df['key'] = 1  # Temporary key column for cross join

    # Perform the cross join using merge
    cross_join_df = pd.merge(drugs_df, publications_df, on='key')

    # Filter where the drug name appears
    # mask = cross_join_df['title_lower'].str.contains(cross_join_df['drug_lower'], na=False)
    # Apply an element-wise comparison using a lambda function
    mask = cross_join_df.apply(
        lambda row: row['drug_lower'] in row['title_lower'], axis=1)

    # Select relevant columns
    mentions_df = cross_join_df[mask][['drug', 'journal', 'date', 'id']]
    mentions_df['publication_type'] = publication_type

    return mentions_df

def build_drug_mention_graph(mentions_df: pd.DataFrame) -> list:
    """
    Build a drug mention graph from the dataframe of mentions.
    """
    result = []

    # Group by 'drug'
    for drug, drug_group in mentions_df.groupby('drug'):
        
        # Initialize a list to store mentions for this drug
        mentions = []
        
        # Loop over unique journals in the drug group
        for journal in drug_group['journal'].unique():
            
            # Filter the rows corresponding to the current journal
            journal_group = drug_group[drug_group['journal'] == journal]
            
            # Separate the journal_group into pubmed and clinical_trials references
            pubmed_references = journal_group[journal_group['publication_type'] == 'pubmed']
            clinical_trials_references = journal_group[journal_group['publication_type'] == 'clinical_trials']
            
            # Create a list of references (date and id pairs) for each publication type
            pubmed_refs = [{'date': date, 'id': ref_id} for date, ref_id in zip(pubmed_references['date'], pubmed_references['id'])]
            clinical_trials_refs = [{'date': date, 'id': ref_id} for date, ref_id in zip(clinical_trials_references['date'], clinical_trials_references['id'])]

            # Only add non-empty publication types
            publication_type = {}
            if pubmed_refs:
                publication_type['pubmed'] = pubmed_refs
            if clinical_trials_refs:
                publication_type['clinical_trials'] = clinical_trials_refs

            # Append the current journal and its references to the mentions list
            mentions.append({
                'journal': journal,
                'publication_type': publication_type
            })
        
        # Append the current drug and its mentions to the final result
        result.append({
            'drug': drug,
            'mentions': mentions
        })
    
    return result

