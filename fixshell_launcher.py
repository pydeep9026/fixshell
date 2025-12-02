#!/usr/bin/env python
import sys
import os

def find_fixshell_dir():
    launcher_path = os.path.abspath(__file__)
    launcher_dir = os.path.dirname(launcher_path)
    
    possible_dirs = [
        launcher_dir,
        os.path.join(launcher_dir, 'fixshell'),
        os.path.join(os.path.expanduser('~'), '.local', 'fixshell'),
        os.path.join(os.path.expanduser('~'), 'fixshell'),
        os.path.join(os.path.dirname(launcher_dir), 'fixshell'),
    ]
    
    for dir_path in possible_dirs:
        fixshell_init = os.path.join(dir_path, 'fixshell', '__init__.py')
        if os.path.exists(fixshell_init):
            return dir_path
    
    return launcher_dir

if __name__ == '__main__':
    fixshell_dir = find_fixshell_dir()
    
    if fixshell_dir not in sys.path:
        sys.path.insert(0, fixshell_dir)
    
    try:
        from fixshell.main import main
        main()
    except ImportError as e:
        print(f"Error: Could not import fixshell.")
        print(f"Looking in: {fixshell_dir}")
        print(f"Import error: {e}")
        print(f"\nPlease make sure fixshell is installed correctly.")
        print(f"Run ./setup.sh to install.")
        sys.exit(1)

