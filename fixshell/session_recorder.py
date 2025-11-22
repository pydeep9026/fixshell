import os
import datetime
from .utils import get_sessions_dir

class SessionRecorder:
    def __init__(self, enabled=True):
        self.enabled = enabled
        self.session_file = None
        self.session_started = False
    
    def start_session(self):
        if not self.enabled:
            return
        
        sessions_dir = get_sessions_dir()
        if not os.path.exists(sessions_dir):
            os.makedirs(sessions_dir, exist_ok=True)
        
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        self.session_file = os.path.join(sessions_dir, f'session_{timestamp}.log')
        self.session_started = True
        
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                f.write(f"Session started: {timestamp}\n")
                f.write("=" * 50 + "\n")
        except Exception as e:
            pass
    
    def log_command(self, command, success=True):
        if not self.enabled or not self.session_started or not self.session_file:
            return
        
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        status = '✓' if success else '✗'
        
        try:
            with open(self.session_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} {status} {command}\n")
        except Exception as e:
            pass
    
    def end_session(self):
        if not self.enabled or not self.session_started or not self.session_file:
            return
        
        try:
            with open(self.session_file, 'a', encoding='utf-8') as f:
                f.write("=" * 50 + "\n")
                f.write("Session ended\n")
        except Exception as e:
            pass
        
        self.session_started = False



