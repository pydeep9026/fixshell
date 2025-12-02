import subprocess
import os
import sys
import time

class ShellRunner:
    def __init__(self):
        self.shell_path = self.get_shell_path()
        self.execution_time = 0.0
    
    def get_shell_path(self):
        shell = os.environ.get('SHELL', None)
        if shell:
            return shell
        return '/bin/bash'
    
    def setup_shell_environment(self):
        env = os.environ.copy()
        return env
    
    def execute_command(self, command, shell_path=None):
        if shell_path is None:
            shell_path = self.shell_path
        
        if not command or not command.strip():
            return '', 0, 0
        
        env = self.setup_shell_environment()
        
        start_time = time.time()
        
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                executable=shell_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            stdout, stderr = process.communicate()
            end_time = time.time()
            
            self.execution_time = end_time - start_time
            return_code = process.returncode
            
            output = stdout + stderr if stderr else stdout
            return output, return_code, self.execution_time
        
        except Exception as e:
            end_time = time.time()
            self.execution_time = end_time - start_time
            return f"Error: {str(e)}", 1, self.execution_time
    
    def get_execution_time(self):
        return self.execution_time
    
    def should_show_timer(self, execution_time=None):
        if execution_time is None:
            execution_time = self.execution_time
        return execution_time > 10.0
