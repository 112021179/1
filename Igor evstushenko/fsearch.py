import csv
from fuzzywuzzy import fuzz

def load_valid_symbols(csv_file):
    
    valid_symbols = {}
    with open(csv_file, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            valid_symbols[row["Symbol"]] = row["Name"]
    return valid_symbols

def find_similar_symbols(input_text, valid_symbols):
    similarity_scores = []
    
    for symbol, company in valid_symbols.items():
        symbol_score = fuzz.ratio(input_text.upper(), symbol.upper())
        company_score = fuzz.ratio(input_text.upper(), company.upper())
        best_score = max(symbol_score, company_score)
        similarity_scores.append((symbol, company, best_score))
    
    best_matches = sorted(similarity_scores, key=lambda item: item[2], reverse=True)[:5]
    return best_matches