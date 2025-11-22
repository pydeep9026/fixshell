import json
import os
import re
from .utils import get_data_dir

class DangerDetector:
    def __init__(self, patterns_file=None):
        if patterns_file is None:
            data_dir = get_data_dir()
            patterns_file = os.path.join(data_dir, 'danger_patterns.json')
        self.patterns_file = patterns_file
        self.patterns = []
        self.load_danger_patterns()
    
    def load_danger_patterns(self):
        if not os.path.exists(self.patterns_file):
            self.patterns = []
            return
        
        try:
            with open(self.patterns_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.patterns = data.get('patterns', [])
        except Exception as e:
            self.patterns = []
    
    def check_danger(self, command):
        if not command or not self.patterns:
            return None
        
        command_lower = command.lower()
        
        for pattern_info in self.patterns:
            pattern = pattern_info.get('pattern', '')
            reason = pattern_info.get('reason', 'Unknown danger')
            severity = pattern_info.get('severity', 'medium')
            
            try:
                if re.search(pattern, command, re.IGNORECASE):
                    return {
                        'dangerous': True,
                        'reason': reason,
                        'severity': severity,
                        'pattern': pattern
                    }
            except re.error:
                if pattern.lower() in command_lower:
                    return {
                        'dangerous': True,
                        'reason': reason,
                        'severity': severity,
                        'pattern': pattern
                    }
        
        return None
    
    def show_danger_warning(self, command, danger_info):
        reason = danger_info.get('reason', 'Unknown danger')
        severity = danger_info.get('severity', 'medium')
        
        severity_emoji = {
            'critical': '🔴',
            'high': '🟠',
            'medium': '🟡',
            'low': '🟢'
        }
        
        emoji = severity_emoji.get(severity, '⚠️')
        print(f"\n{emoji}  This command is destructive — {reason}")
        print(f"Command: {command}")
        print("Confirm? (y/n): ", end='', flush=True)



