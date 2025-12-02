import os
import json
import subprocess
import re
from .utils import get_data_dir

class HelpIndexBuilder:
    def __init__(self):
        self.help_cache_dir = os.path.join(get_data_dir(), 'help_cache')
        os.makedirs(self.help_cache_dir, exist_ok=True)
    
    def build_help_index(self, command_name):
        cache_file = os.path.join(self.help_cache_dir, f'{command_name}.json')
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        try:
            result = subprocess.run(
                [command_name, '--help'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            help_text = result.stdout + result.stderr
            parsed = self.parse_help_output(command_name, help_text)
            
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(parsed, f, indent=2)
            
            return parsed
        except Exception as e:
            return None
    
    def parse_help_output(self, command_name, help_text):
        flags = {}
        lines = help_text.split('\n')
        
        current_section = None
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            flag_match = re.match(r'^\s*([-]{1,2}[\w-]+(?:\[?=?\w*\]?)?)\s+(.+)', line)
            if flag_match:
                flag = flag_match.group(1).strip()
                description = flag_match.group(2).strip()
                flags[flag] = description
        
        return {
            'command': command_name,
            'flags': flags,
            'raw_help': help_text
        }
    
    def get_help_text(self, command_name):
        cache_file = os.path.join(self.help_cache_dir, f'{command_name}.json')
        
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        return self.build_help_index(command_name)
    
    def get_flag_description_from_help(self, command_name, flag):
        help_data = self.get_help_text(command_name)
        if help_data and 'flags' in help_data:
            return help_data['flags'].get(flag, None)
        return None
    
    def update_help_cache(self, command_name):
        return self.build_help_index(command_name)


