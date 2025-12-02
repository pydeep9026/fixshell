import json
import os
from .utils import get_data_dir

class AbbreviationExpander:
    def __init__(self, abbreviations_file=None):
        if abbreviations_file is None:
            data_dir = get_data_dir()
            abbreviations_file = os.path.join(data_dir, 'abbreviations.json')
        self.abbreviations_file = abbreviations_file
        self.abbreviations = {}
        self.load_abbreviations()
    
    def load_abbreviations(self):
        if not os.path.exists(self.abbreviations_file):
            self.abbreviations = {}
            return
        
        try:
            with open(self.abbreviations_file, 'r', encoding='utf-8') as f:
                self.abbreviations = json.load(f)
        except Exception as e:
            self.abbreviations = {}
    
    def find_abbreviation_match(self, token):
        return self.abbreviations.get(token, None)
    
    def expand_abbreviation(self, input_text):
        tokens = input_text.split()
        if not tokens:
            return input_text, False
        
        first_token = tokens[0]
        expansion = self.find_abbreviation_match(first_token)
        
        if expansion:
            remaining_text = ' '.join(tokens[1:]) if len(tokens) > 1 else ''
            expanded = expansion + (' ' + remaining_text if remaining_text else '')
            return expanded, True
        
        return input_text, False
    
    def add_abbreviation(self, alias, command):
        self.abbreviations[alias] = command
        self.save_abbreviations()
    
    def save_abbreviations(self):
        try:
            with open(self.abbreviations_file, 'w', encoding='utf-8') as f:
                json.dump(self.abbreviations, f, indent=2)
        except Exception as e:
            pass



