import difflib
from .command_loader import CommandLoader

class CommandSuggester:
    def __init__(self, command_loader):
        self.command_loader = command_loader
        self.threshold = 0.7
    
    def get_best_match(self, token, candidates, threshold=None):
        if threshold is None:
            threshold = self.threshold
        
        if not candidates:
            return None
        
        matches = difflib.get_close_matches(token, candidates, n=1, cutoff=threshold)
        if matches:
            return matches[0]
        return None
    
    def detect_typo_in_command(self, input_text, command_db=None):
        if command_db is None:
            command_db = self.command_loader.commands_db
        
        tokens = input_text.split()
        if not tokens:
            return None
        
        first_token = tokens[0]
        all_commands = self.command_loader.get_all_commands()
        match = self.get_best_match(first_token, all_commands)
        
        if match and match != first_token:
            return {
                'token': first_token,
                'suggestion': match,
                'type': 'command',
                'position': 0
            }
        
        if first_token in command_db and len(tokens) > 1:
            subcommands = self.command_loader.get_subcommands(first_token)
            if subcommands:
                match = self.get_best_match(tokens[1], subcommands)
                if match and match != tokens[1]:
                    return {
                        'token': tokens[1],
                        'suggestion': match,
                        'type': 'subcommand',
                        'position': 1
                    }
        
        return None
    
    def detect_typo_in_flags(self, input_text, command_db=None):
        if command_db is None:
            command_db = self.command_loader.commands_db
        
        tokens = input_text.split()
        if len(tokens) < 2:
            return None
        
        command_name = tokens[0]
        if command_name not in command_db:
            return None
        
        subcommands = self.command_loader.get_subcommands(command_name)
        subcommand = None
        flag_start = 1
        
        if len(tokens) > 1 and tokens[1] in subcommands:
            subcommand = tokens[1]
            flag_start = 2
        
        flags = self.command_loader.get_flags(command_name, subcommand)
        if not flags or not isinstance(flags, dict):
            return None
        
        available_flags = list(flags.keys())
        
        for i in range(flag_start, len(tokens)):
            token = tokens[i]
            if token.startswith('-'):
                match = self.get_best_match(token, available_flags)
                if match and match != token:
                    return {
                        'token': token,
                        'suggestion': match,
                        'type': 'flag',
                        'position': i
                    }
        
        return None
    
    def suggest_correction(self, input_text):
        command_typo = self.detect_typo_in_command(input_text)
        if command_typo:
            return command_typo
        
        flag_typo = self.detect_typo_in_flags(input_text)
        if flag_typo:
            return flag_typo
        
        return None
    
    def apply_correction(self, input_text, suggestion):
        tokens = input_text.split()
        if suggestion['position'] < len(tokens):
            tokens[suggestion['position']] = suggestion['suggestion']
            return ' '.join(tokens)
        return input_text

