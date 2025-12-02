import json
import os
from .utils import get_data_dir

class CommandLoader:
    def __init__(self, commands_file=None):
        if commands_file is None:
            data_dir = get_data_dir()
            commands_file = os.path.join(data_dir, 'commands.json')
        self.commands_file = commands_file
        self.commands_db = {}
        self.load_commands()
    
    def load_commands(self):
        if not os.path.exists(self.commands_file):
            self.commands_db = {}
            return
        
        try:
            with open(self.commands_file, 'r', encoding='utf-8') as f:
                self.commands_db = json.load(f)
        except Exception as e:
            self.commands_db = {}
    
    def get_command_info(self, command_name):
        return self.commands_db.get(command_name, {})
    
    def get_subcommands(self, command_name):
        cmd_info = self.get_command_info(command_name)
        return cmd_info.get('subcommands', [])
    
    def get_flags(self, command_name, subcommand=None):
        cmd_info = self.get_command_info(command_name)
        flags = cmd_info.get('flags', {})
        
        if subcommand and subcommand in flags:
            return flags[subcommand]
        elif 'global' in flags:
            return flags['global']
        return {}
    
    def get_flag_description(self, command_name, flag, subcommand=None):
        flags = self.get_flags(command_name, subcommand)
        if isinstance(flags, dict):
            return flags.get(flag, None)
        return None
    
    def get_all_commands(self):
        return list(self.commands_db.keys())
    
    def has_command(self, command_name):
        return command_name in self.commands_db



