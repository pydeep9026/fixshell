import json
import os
import re
from .utils import get_data_dir

class SnippetManager:
    def __init__(self, snippets_file=None):
        if snippets_file is None:
            data_dir = get_data_dir()
            snippets_file = os.path.join(data_dir, 'snippets.json')
        self.snippets_file = snippets_file
        self.snippets = {}
        self.load_snippets()
    
    def load_snippets(self):
        if not os.path.exists(self.snippets_file):
            self.snippets = {}
            return
        
        try:
            with open(self.snippets_file, 'r', encoding='utf-8') as f:
                self.snippets = json.load(f)
        except Exception as e:
            self.snippets = {}
    
    def parse_snippet_args(self, input_text):
        tokens = input_text.split()
        if not tokens:
            return None, []
        
        snippet_name = tokens[0]
        args = tokens[1:] if len(tokens) > 1 else []
        return snippet_name, args
    
    def expand_snippet(self, snippet_name, args=None):
        if snippet_name not in self.snippets:
            return None, False
        
        template = self.snippets[snippet_name]
        
        if args is None:
            args = []
        
        placeholders = re.findall(r'\{(\w+)\}', template)
        
        if not placeholders:
            return template, True
        
        result = template
        for i, placeholder in enumerate(placeholders):
            value = args[i] if i < len(args) else ''
            result = result.replace(f'{{{placeholder}}}', value)
        
        remaining_placeholders = re.findall(r'\{(\w+)\}', result)
        if remaining_placeholders:
            return None, False
        
        return result, True
    
    def save_snippet(self, name, template):
        self.snippets[name] = template
        self.save_snippets()
    
    def save_snippets(self):
        try:
            with open(self.snippets_file, 'w', encoding='utf-8') as f:
                json.dump(self.snippets, f, indent=2)
        except Exception as e:
            pass
    
    def has_snippet(self, snippet_name):
        return snippet_name in self.snippets
    
    def expand_input(self, input_text):
        snippet_name, args = self.parse_snippet_args(input_text)
        if snippet_name and self.has_snippet(snippet_name):
            expanded, success = self.expand_snippet(snippet_name, args)
            if success:
                return expanded, True
        return input_text, False



