import os
import difflib

class HistorySearch:
    def __init__(self):
        self.history = []
        self.history_file = self.get_history_file()
        self.load_history()
    
    def get_history_file(self):
        home = os.path.expanduser('~')
        shell = os.environ.get('SHELL', '')
        
        if 'zsh' in shell.lower():
            return os.path.join(home, '.zsh_history')
        elif 'bash' in shell.lower():
            return os.path.join(home, '.bash_history')
        else:
            return os.path.join(home, '.bash_history')
    
    def load_history(self):
        if not os.path.exists(self.history_file):
            self.history = []
            return
        
        try:
            with open(self.history_file, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
                self.history = [line.strip() for line in lines if line.strip()]
        except Exception as e:
            self.history = []
    
    def search_history(self, query, limit=10):
        if not query or not self.history:
            return []
        
        matches = difflib.get_close_matches(query, self.history, n=limit, cutoff=0.3)
        return matches
    
    def add_to_history(self, command):
        if command and command not in self.history:
            self.history.append(command)
            if len(self.history) > 10000:
                self.history = self.history[-10000:]



