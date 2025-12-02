import os
import sys
import shutil
import re

def get_terminal_size():
    try:
        cols, rows = shutil.get_terminal_size()
        return cols, rows
    except:
        return 80, 24

def clear_screen():
    os.system('clear')

def escape_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def format_suggestion(text, correction):
    return f"{text} → {correction}"

def get_data_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, 'data')

def get_themes_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, 'themes')

def get_sessions_dir():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    return os.path.join(project_root, 'sessions')