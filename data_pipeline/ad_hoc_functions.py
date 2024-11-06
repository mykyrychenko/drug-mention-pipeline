from collections import defaultdict

def journal_with_most_unique_drugs(drug_mentions_graph: list) -> tuple:
    """
    Extracts the journal that mentions the most distinct drugs
    """
    # Dictionary to track unique drugs for each journal
    journal_drug_map = defaultdict(set)

    # Populate journal_drug_map with drugs mentioned in each journal
    for entry in drug_mentions_graph:
        drug = entry['drug']
        for mention in entry['mentions']:
            journal = mention['journal']
            journal_drug_map[journal].add(drug)

    # Find the journal with the maximum number of unique drugs
    most_drug_journal = max(journal_drug_map, key=lambda k: len(journal_drug_map[k]))
    return most_drug_journal, len(journal_drug_map[most_drug_journal])

def find_related_drugs(drug_mentions_graph: list, target_drug: str, target_publication_type: str) -> set:
    """
    Find all drugs mentioned in the same journals as the target drug in publication
    """
    # Identify journals for the target drug in target publication type
    target_drug_journals = identify_journals_for_drug(drug_mentions_graph, target_drug, target_publication_type)

    # Find other drugs mentioned in the same journals for target publication type
    related_drugs = set()
    for entry in drug_mentions_graph:
        if entry['drug'] == target_drug:
            continue  # Skip the target drug itself
        for mention in entry['mentions']:
            # Check if the journal is one of the target drug's journals and target publication type mentions
            if mention['journal'] in target_drug_journals and target_publication_type in mention['publication_type']:
                related_drugs.add(entry['drug'])

    return related_drugs

def identify_journals_for_drug(drug_mentions_graph: list, target_drug: str, target_publication_type: str) -> set:
    """
    Identify journals for the target drug in publications
    """
    target_drug_journals = set()
    for entry in drug_mentions_graph:
        if entry['drug'] == target_drug:
            for mention in entry['mentions']:
                # Check if the journal has pubmed mentions and not clinical trials
                if target_publication_type in mention['publication_type']:
                    target_drug_journals.add(mention['journal'])
            break
    
    return target_drug_journals