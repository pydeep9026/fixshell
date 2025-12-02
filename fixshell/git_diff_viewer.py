import re

class GitDiffViewer:
    def __init__(self):
        self.diff_patterns = [
            r'^diff --git',
            r'^index [a-f0-9]+\.\.[a-f0-9]+',
            r'^---',
            r'^\+\+\+',
            r'^@@',
            r'^[-+ ]',
        ]
    
    def is_git_diff_command(self, command):
        git_diff_commands = [
            'git diff',
            'git show',
            'git log -p',
            'git diff --cached',
            'git diff --staged',
        ]
        
        command_lower = command.lower()
        return any(cmd in command_lower for cmd in git_diff_commands)
    
    def parse_diff_output(self, output):
        if not output:
            return None
        
        lines = output.split('\n')
        if not any(re.match(r'^diff --git', line) for line in lines[:10]):
            return None
        
        return self.format_diff(output)
    
    def format_diff(self, diff_text):
        lines = diff_text.split('\n')
        formatted = []
        
        for line in lines:
            if line.startswith('diff --git'):
                formatted.append(f'\033[1m\033[36m{line}\033[0m')
            elif line.startswith('index '):
                formatted.append(f'\033[90m{line}\033[0m')
            elif line.startswith('---'):
                formatted.append(f'\033[31m{line}\033[0m')
            elif line.startswith('+++'):
                formatted.append(f'\033[32m{line}\033[0m')
            elif line.startswith('@@'):
                formatted.append(f'\033[33m{line}\033[0m')
            elif line.startswith('-') and not line.startswith('---'):
                formatted.append(f'\033[31m{line}\033[0m')
            elif line.startswith('+') and not line.startswith('+++'):
                formatted.append(f'\033[32m{line}\033[0m')
            else:
                formatted.append(line)
        
        return '\n'.join(formatted)
    
    def display_diff(self, output):
        formatted = self.parse_diff_output(output)
        if formatted:
            return formatted
        return output


