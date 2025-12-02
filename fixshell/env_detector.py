import os
import subprocess

class EnvDetector:
    def __init__(self):
        pass
    
    def detect_python_project(self, cwd=None):
        if cwd is None:
            cwd = os.getcwd()
        
        indicators = [
            'requirements.txt',
            'setup.py',
            'Pipfile',
            'pyproject.toml',
            'poetry.lock',
            'Pipfile.lock'
        ]
        
        for indicator in indicators:
            if os.path.exists(os.path.join(cwd, indicator)):
                return True
        
        return False
    
    def check_venv_activated(self):
        return 'VIRTUAL_ENV' in os.environ or 'CONDA_DEFAULT_ENV' in os.environ
    
    def find_venv_path(self, cwd=None):
        if cwd is None:
            cwd = os.getcwd()
        
        possible_paths = [
            os.path.join(cwd, 'venv'),
            os.path.join(cwd, '.venv'),
            os.path.join(cwd, 'env'),
            os.path.join(cwd, '.env')
        ]
        
        for path in possible_paths:
            if os.path.exists(path) and os.path.isdir(path):
                return path
        
        return None
    
    def prompt_activate_venv(self, venv_path):
        print(f"\n⚠️  Virtual environment not activated")
        print(f"Virtualenv found at: {venv_path}")
        print("Activate? (y/n): ", end='', flush=True)
    
    def should_prompt(self, cwd=None):
        if self.check_venv_activated():
            return False
        
        if not self.detect_python_project(cwd):
            return False
        
        venv_path = self.find_venv_path(cwd)
        return venv_path is not None
