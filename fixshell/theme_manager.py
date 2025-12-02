import json
import os
from .utils import get_themes_dir

class ThemeManager:
    def __init__(self, theme_name='default'):
        self.themes_dir = get_themes_dir()
        self.current_theme = None
        self.theme_name = theme_name
        self.load_theme(theme_name)
    
    def load_theme(self, theme_name):
        theme_file = os.path.join(self.themes_dir, f'{theme_name}.json')
        
        if not os.path.exists(theme_file):
            self.current_theme = self.get_default_theme()
            return
        
        try:
            with open(theme_file, 'r', encoding='utf-8') as f:
                self.current_theme = json.load(f)
        except Exception as e:
            self.current_theme = self.get_default_theme()
    
    def get_default_theme(self):
        return {
            'name': 'default',
            'colors': {
                'background': '#000000',
                'foreground': '#ffffff',
                'suggestion': '#00ff00',
                'error': '#ff0000',
                'warning': '#ffff00',
                'info': '#00ffff'
            }
        }
    
    def get_color(self, element):
        if not self.current_theme:
            return ''
        
        colors = self.current_theme.get('colors', {})
        return colors.get(element, '')
    
    def apply_theme(self, theme_name):
        self.theme_name = theme_name
        self.load_theme(theme_name)
    
    def list_themes(self):
        if not os.path.exists(self.themes_dir):
            return ['default']
        
        themes = []
        for file in os.listdir(self.themes_dir):
            if file.endswith('.json'):
                themes.append(file[:-5])
        
        return themes if themes else ['default']



