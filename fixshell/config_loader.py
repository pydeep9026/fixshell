import json
import os
from .utils import get_data_dir

class ConfigLoader:
    def __init__(self, config_file=None):
        if config_file is None:
            data_dir = get_data_dir()
            config_file = os.path.join(data_dir, 'config.json')
        self.config_file = config_file
        self.config = self.load_config()
    
    def load_config(self):
        default_config = {
            "show_suggestions": True,
            "auto_correct": False,
            "session_recording": True,
            "danger_detection": True,
            "env_detection": True,
            "command_timer": True,
            "flag_descriptions": True
        }
        
        if not os.path.exists(self.config_file):
            self.save_config(default_config)
            return default_config
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                default_config.update(user_config)
                return default_config
        except Exception as e:
            return default_config
    
    def save_config(self, config=None):
        if config is None:
            config = self.config
        
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            pass
    
    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save_config()


