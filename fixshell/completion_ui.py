import sys
import os
from .utils import get_terminal_size

class CompletionUI:
    def __init__(self, command_loader):
        self.command_loader = command_loader
        self.completions = []
        self.selected_index = 0
        self.visible = False
    
    def get_completions(self, buffer):
        if not buffer or not buffer.strip():
            return []
        
        tokens = buffer.split()
        if not tokens:
            return []
        
        last_token = tokens[-1]
        command_name = tokens[0] if len(tokens) > 0 else ''
        
        completions = []
        
        if len(tokens) == 1:
            all_commands = self.command_loader.get_all_commands()
            for cmd in all_commands:
                if cmd.startswith(last_token):
                    completions.append(cmd)
        elif command_name in self.command_loader.commands_db:
            if len(tokens) == 2:
                subcommands = self.command_loader.get_subcommands(command_name)
                for subcmd in subcommands:
                    if subcmd.startswith(last_token):
                        completions.append(subcmd)
            else:
                subcommand = tokens[1] if len(tokens) > 1 else None
                flags = self.command_loader.get_flags(command_name, subcommand)
                if isinstance(flags, dict):
                    for flag in flags.keys():
                        if flag.startswith(last_token):
                            completions.append(flag)
        
        return completions[:10]
    
    def show_completions(self, buffer, cursor_pos):
        self.completions = self.get_completions(buffer)
        if not self.completions:
            self.visible = False
            return
        
        self.selected_index = 0
        self.visible = True
        self.render_completions(buffer, cursor_pos)
    
    def hide_completions(self):
        self.visible = False
        self.completions = []
        self.selected_index = 0
    
    def render_completions(self, buffer, cursor_pos):
        if not self.visible or not self.completions:
            return
        
        cols, rows = get_terminal_size()
        prompt_len = len(buffer) + 20
        
        sys.stdout.write('\n')
        for i, completion in enumerate(self.completions[:5]):
            if i == self.selected_index:
                sys.stdout.write(f'\033[47m\033[30m→ {completion}\033[0m\n')
            else:
                sys.stdout.write(f'  {completion}\n')
        sys.stdout.flush()
    
    def navigate_up(self):
        if self.selected_index > 0:
            self.selected_index -= 1
    
    def navigate_down(self):
        if self.selected_index < len(self.completions) - 1:
            self.selected_index += 1
    
    def get_selected(self):
        if self.completions and 0 <= self.selected_index < len(self.completions):
            return self.completions[self.selected_index]
        return None


