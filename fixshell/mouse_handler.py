import sys
import os

class MouseHandler:
    def __init__(self):
        self.mouse_enabled = False
        self.terminal_supports_mouse = self.check_terminal_support()
    
    def check_terminal_support(self):
        return True
    
    def enable_mouse_mode(self):
        if not self.terminal_supports_mouse:
            return False
        
        try:
            sys.stdout.write('\033[?1000h')
            sys.stdout.write('\033[?1002h')
            sys.stdout.write('\033[?1015h')
            sys.stdout.write('\033[?1006h')
            sys.stdout.flush()
            self.mouse_enabled = True
            return True
        except:
            return False
    
    def disable_mouse_mode(self):
        if not self.mouse_enabled:
            return
        
        try:
            sys.stdout.write('\033[?1006l')
            sys.stdout.write('\033[?1015l')
            sys.stdout.write('\033[?1002l')
            sys.stdout.write('\033[?1000l')
            sys.stdout.flush()
            self.mouse_enabled = False
        except:
            pass
    
    def parse_mouse_event(self, data):
        if not data.startswith('\033['):
            return None
        
        if data.startswith('\033[<'):
            parts = data[3:].rstrip('mM').split(';')
            if len(parts) >= 3:
                try:
                    buttons = int(parts[0])
                    x = int(parts[1])
                    y = int(parts[2])
                    
                    click_type = 'left' if buttons == 0 else 'right' if buttons == 2 else 'middle'
                    return {
                        'type': 'click',
                        'button': click_type,
                        'x': x,
                        'y': y,
                        'buttons': buttons
                    }
                except:
                    return None
        
        return None
    
    def calculate_cursor_position(self, click_x, click_y, prompt_length, buffer_length, terminal_width):
        if click_y == 1:
            input_line_pos = click_x - prompt_length - 1
            if 0 <= input_line_pos <= buffer_length:
                return input_line_pos
        return None


