import sys
import os
import select
import termios
import tty
import re

class InputWithMouse:
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = None
        self.buffer = ''
        self.cursor_pos = 0
    
    def enable_raw(self):
        if self.old_settings is None:
            self.old_settings = termios.tcgetattr(self.fd)
            tty.setraw(self.fd)
    
    def disable_raw(self):
        if self.old_settings is not None:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
            self.old_settings = None
    
    def has_input(self, timeout=0):
        return select.select([sys.stdin], [], [], timeout) == ([sys.stdin], [], [])
    
    def read_char(self):
        if not self.has_input():
            return None
        try:
            return sys.stdin.read(1)
        except:
            return None
    
    def read_sequence(self, max_chars=20):
        seq = ''
        for _ in range(max_chars):
            if not self.has_input(0.05):
                break
            char = self.read_char()
            if char is None:
                break
            seq += char
            if char.isalpha() or char in 'mM':
                break
        return seq
    
    def parse_mouse_event(self, seq):
        if not seq.startswith('<'):
            return None
        
        parts = seq[1:].rstrip('mM').split(';')
        if len(parts) >= 3:
            try:
                buttons = int(parts[0])
                x = int(parts[1])
                y = int(parts[2])
                return {'x': x, 'y': y, 'button': buttons}
            except:
                pass
        return None
    
    def strip_ansi(self, text):
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text)
    
    def read_line_with_mouse(self, prompt, mouse_enabled=False):
        self.enable_raw()
        buffer = ''
        cursor_pos = 0
        prompt_plain = self.strip_ansi(prompt)
        prompt_len = len(prompt_plain)
        
        try:
            while True:
                sys.stdout.write('\r')
                sys.stdout.write('\033[K')
                sys.stdout.write(prompt)
                sys.stdout.write(buffer)
                
                cursor_abs_pos = prompt_len + cursor_pos
                if cursor_abs_pos > 0:
                    sys.stdout.write(f'\033[{cursor_abs_pos + 1}G')
                sys.stdout.flush()
                
                char = self.read_char()
                if char is None:
                    continue
                
                if char == '\r' or char == '\n':
                    self.disable_raw()
                    print()
                    return buffer
                
                elif char == '\x03':
                    self.disable_raw()
                    print()
                    raise KeyboardInterrupt
                
                elif char == '\x7f' or char == '\x08':
                    if cursor_pos > 0:
                        buffer = buffer[:cursor_pos-1] + buffer[cursor_pos:]
                        cursor_pos -= 1
                
                elif char == '\x1b':
                    next_char = self.read_char()
                    if next_char is None:
                        continue
                    
                    if next_char == '[':
                        third = self.read_char()
                        if third is None:
                            continue
                        
                        if third == '<' and mouse_enabled:
                            seq = self.read_sequence(20)
                            mouse_event = self.parse_mouse_event(third + seq)
                            if mouse_event:
                                click_x = mouse_event['x']
                                click_y = mouse_event['y']
                                button = mouse_event['button']
                                
                                if button == 0 and click_y == 1:
                                    new_pos = click_x - prompt_len - 1
                                    cursor_pos = max(0, min(len(buffer), new_pos))
                        
                        elif third == 'D':
                            if cursor_pos > 0:
                                cursor_pos -= 1
                        elif third == 'C':
                            if cursor_pos < len(buffer):
                                cursor_pos += 1
                        elif third == 'A':
                            pass
                        elif third == 'B':
                            pass
                        else:
                            rest = self.read_sequence(15)
                            if rest and mouse_enabled:
                                full_seq = third + rest
                                if '<' in full_seq:
                                    try:
                                        mouse_idx = full_seq.index('<')
                                        mouse_part = full_seq[mouse_idx:]
                                        mouse_event = self.parse_mouse_event(mouse_part)
                                        if mouse_event and mouse_event['button'] == 0:
                                            click_x = mouse_event['x']
                                            click_y = mouse_event['y']
                                            if click_y == 1:
                                                new_pos = click_x - prompt_len - 1
                                                cursor_pos = max(0, min(len(buffer), new_pos))
                                    except:
                                        pass
                
                elif ord(char) >= 32 and ord(char) < 127:
                    buffer = buffer[:cursor_pos] + char + buffer[cursor_pos:]
                    cursor_pos += 1
        
        finally:
            self.disable_raw()

