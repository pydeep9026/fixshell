import sys
import os
import subprocess
import shutil
from .utils import get_terminal_size, clear_screen

try:
    import select
    import termios
    import tty
    HAS_TERMIOS = True
except ImportError:
    HAS_TERMIOS = False

class EditorWithCommands:
    def __init__(self, file_path):
        self.file_path = file_path
        self.lines = []
        self.cursor_line = 0
        self.cursor_col = 0  # Column position within line
        self.selected_lines = set()
        self.clipboard = []
        self.search_term = None
        self.search_results = []
        self.current_search_idx = -1
        
        if not os.path.exists(file_path):
            self.lines = ['']
        else:
            try:
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    self.lines = f.readlines()
                if not self.lines:
                    self.lines = ['']
            except Exception as e:
                self.lines = [f"Error reading file: {str(e)}"]
        
        for i in range(len(self.lines)):
            if self.lines[i].endswith('\n'):
                self.lines[i] = self.lines[i][:-1]
        
        if not self.lines:
            self.lines = ['']
        
        # Ensure cursor position is valid
        self._clamp_cursor()
    
    def _clamp_cursor(self):
        """Ensure cursor position is valid"""
        if self.cursor_line < 0:
            self.cursor_line = 0
        if self.cursor_line >= len(self.lines):
            self.cursor_line = max(0, len(self.lines) - 1)
        line_len = len(self.lines[self.cursor_line])
        if self.cursor_col < 0:
            self.cursor_col = 0
        if self.cursor_col > line_len:
            self.cursor_col = line_len
    
    def detect_editor(self):
        editors = ['vim', 'nano', 'vi']
        for editor in editors:
            if shutil.which(editor):
                return editor
        return None
    
    def open_in_editor(self, line_num=None):
        """Open file in vim/nano at specific line"""
        editor = self.detect_editor()
        if not editor:
            return False
        
        try:
            if editor == 'vim':
                cmd = ['vim']
                if line_num:
                    cmd.extend(['+', str(line_num)])
                cmd.append(self.file_path)
            elif editor == 'nano':
                cmd = ['nano']
                if line_num:
                    cmd.extend(['+', str(line_num)])
                cmd.append(self.file_path)
            else:
                cmd = [editor, self.file_path]
                if line_num:
                    cmd.extend(['+', str(line_num)])
            
            subprocess.Popen(
                cmd,
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr
            ).wait()
            
            # Reload file after editing
            self.reload_file()
            return True
        except Exception:
            return False
    
    def reload_file(self):
        """Reload file from disk"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8', errors='replace') as f:
                    self.lines = f.readlines()
                for i in range(len(self.lines)):
                    if self.lines[i].endswith('\n'):
                        self.lines[i] = self.lines[i][:-1]
                if not self.lines:
                    self.lines = ['']
            except:
                pass
    
    def render(self):
        """Render file with line numbers"""
        cols, rows = get_terminal_size()
        edit_rows = rows - 5
        
        sys.stdout.write('\033[2J\033[H')
        sys.stdout.flush()
        
        header = f"\033[1m\033[36mEditor\033[0m - {os.path.basename(self.file_path)}"
        header += f" | Line {self.cursor_line + 1}/{len(self.lines)}"
        if self.selected_lines:
            header += f" | \033[33m{len(self.selected_lines)} selected\033[0m"
        if self.search_term:
            header += f" | \033[35mSearch: {self.search_term}\033[0m"
        print(header)
        print("\033[1m" + "=" * cols + "\033[0m")
        
        max_line_num = len(self.lines)
        line_num_width = max(4, len(str(max_line_num)))
        
        visible_start = max(0, self.cursor_line - edit_rows // 2)
        visible_end = min(visible_start + edit_rows, len(self.lines))
        
        for i in range(visible_start, visible_end):
            line = self.lines[i] if i < len(self.lines) else ''
            line_num = i + 1
            line_num_str = str(line_num).rjust(line_num_width)
            
            max_line_len = cols - line_num_width - 6
            if max_line_len < 1:
                max_line_len = 1
            
            display_line = line[:max_line_len] if len(line) > max_line_len else line
            if len(line) > max_line_len:
                display_line += '\033[90m>\033[0m'
            
            is_selected = i in self.selected_lines
            is_cursor = i == self.cursor_line
            is_search_match = self.search_term and i in self.search_results
            
            if is_cursor:
                # Show cursor position within line
                cursor_pos = min(self.cursor_col, max_line_len)
                if cursor_pos < len(display_line):
                    # Insert cursor marker at cursor position
                    before_cursor = display_line[:cursor_pos]
                    cursor_char = display_line[cursor_pos] if cursor_pos < len(display_line) else ' '
                    after_cursor = display_line[cursor_pos + 1:] if cursor_pos + 1 < len(display_line) else ''
                    display_line = before_cursor + f'\033[7m{cursor_char}\033[0m' + after_cursor
                elif cursor_pos >= len(line):
                    # Cursor beyond visible line end
                    display_line = display_line + '\033[7m \033[0m'
                
                prefix = "\033[1m\033[32m>\033[0m \033[1m\033[32m"
                suffix = "\033[0m"
                line_style = ""
            elif is_selected:
                prefix = "  \033[1m\033[33m"
                suffix = "\033[0m"
                line_style = "\033[43m\033[30m"
            elif is_search_match:
                prefix = "  "
                suffix = ""
                line_style = "\033[46m\033[30m"
            else:
                prefix = "  "
                suffix = ""
                line_style = ""
            
            # Ensure we print something even if line is empty
            if line_style:
                print(f"{prefix}{line_num_str}\033[0m | {line_style}{display_line or ' '}\033[0m{suffix}")
            else:
                print(f"{prefix}{line_num_str}\033[0m | {display_line or ' '}{suffix}")
        
        if len(self.lines) > visible_end:
            remaining = len(self.lines) - visible_end
            print(f"\033[90m... {remaining} more lines\033[0m")
        
        print("\033[1m" + "=" * cols + "\033[0m")
        # Command hint (will be overwritten if in command mode)
        if not hasattr(self, '_in_command_mode') or not self._in_command_mode:
            print("\033[90mCommands: :jump <n> :select <n> :copy :search <term> :edit [line] :quit | Arrow keys: navigate\033[0m")
    
    def jump_to_line(self, line_num):
        if 1 <= line_num <= len(self.lines):
            self.cursor_line = line_num - 1
            self.cursor_col = 0  # Reset to start of line
            self._clamp_cursor()
            return True
        return False
    
    def move_up(self):
        """Move cursor up one line"""
        if self.cursor_line > 0:
            self.cursor_line -= 1
            self._clamp_cursor()
    
    def move_down(self):
        """Move cursor down one line"""
        if self.cursor_line < len(self.lines) - 1:
            self.cursor_line += 1
            self._clamp_cursor()
    
    def move_left(self):
        """Move cursor left one character"""
        if self.cursor_col > 0:
            self.cursor_col -= 1
        elif self.cursor_line > 0:
            # Move to end of previous line
            self.cursor_line -= 1
            self.cursor_col = len(self.lines[self.cursor_line])
        self._clamp_cursor()
    
    def move_right(self):
        """Move cursor right one character"""
        line_len = len(self.lines[self.cursor_line])
        if self.cursor_col < line_len:
            self.cursor_col += 1
        elif self.cursor_line < len(self.lines) - 1:
            # Move to start of next line
            self.cursor_line += 1
            self.cursor_col = 0
        self._clamp_cursor()
    
    def insert_char(self, char):
        """Insert character at cursor position"""
        line = self.lines[self.cursor_line]
        self.lines[self.cursor_line] = line[:self.cursor_col] + char + line[self.cursor_col:]
        self.cursor_col += 1
    
    def delete_char_backward(self):
        """Delete character before cursor"""
        line = self.lines[self.cursor_line]
        if self.cursor_col > 0:
            self.lines[self.cursor_line] = line[:self.cursor_col-1] + line[self.cursor_col:]
            self.cursor_col -= 1
        elif self.cursor_line > 0:
            # Merge with previous line
            prev_len = len(self.lines[self.cursor_line - 1])
            self.lines[self.cursor_line - 1] += self.lines[self.cursor_line]
            del self.lines[self.cursor_line]
            self.cursor_line -= 1
            self.cursor_col = prev_len
        self._clamp_cursor()
    
    def select_line(self, line_num):
        idx = line_num - 1
        if 0 <= idx < len(self.lines):
            if idx in self.selected_lines:
                self.selected_lines.remove(idx)
            else:
                self.selected_lines.add(idx)
            return True
        return False
    
    def search(self, term):
        import re
        self.search_term = term
        self.search_results = []
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        for i, line in enumerate(self.lines):
            if pattern.search(line):
                self.search_results.append(i)
        if self.search_results:
            self.current_search_idx = 0
            self.cursor_line = self.search_results[0]
            return f'Found {len(self.search_results)} matches'
        return f'No matches found'
    
    def next_search(self):
        if self.search_results:
            self.current_search_idx = (self.current_search_idx + 1) % len(self.search_results)
            self.cursor_line = self.search_results[self.current_search_idx]
    
    def copy_selected(self):
        if self.selected_lines:
            self.clipboard = [self.lines[i] for i in sorted(self.selected_lines)]
            return f'Copied {len(self.clipboard)} line(s)'
        return 'No lines selected'
    
    def execute_command(self, cmd):
        parts = cmd.split()
        if not parts:
            return None
        
        command = parts[0].lower()
        
        if command in ('j', 'jump'):
            if len(parts) < 2:
                return 'Usage: :jump <line_number>'
            try:
                line_num = int(parts[1])
                if self.jump_to_line(line_num):
                    return f'Jumped to line {line_num}'
                return 'Invalid line number'
            except ValueError:
                return 'Line number must be integer'
        
        elif command in ('s', 'search'):
            if len(parts) < 2:
                return 'Usage: :search <term>'
            term = ' '.join(parts[1:])
            return self.search(term)
        
        elif command in ('n', 'next'):
            if self.search_results:
                self.next_search()
                return f'Match {self.current_search_idx + 1}/{len(self.search_results)}'
            return 'No search active'
        
        elif command in ('sel', 'select'):
            if len(parts) < 2:
                return 'Usage: :select <line_number>'
            try:
                line_num = int(parts[1])
                self.select_line(line_num)
                return f'Toggled line {line_num}'
            except ValueError:
                return 'Line number must be integer'
        
        elif command == 'copy':
            return self.copy_selected()
        
        elif command in ('edit', 'e'):
            line_num = None
            if len(parts) > 1:
                try:
                    line_num = int(parts[1])
                except ValueError:
                    pass
            if self.open_in_editor(line_num or self.cursor_line + 1):
                return 'File edited - reloaded'
            return 'Failed to open editor'
        
        elif command in ('q', 'quit'):
            return 'quit'
        
        elif command in ('h', 'help'):
            return 'help'
        
        else:
            return f'Unknown command: {command}'
    
    def show_help(self):
        clear_screen()
        help_text = """\033[1m\033[36mEditor Commands\033[0m

\033[1mNavigation:\033[0m
  Arrow keys              - Move cursor
  :jump <n>, :j <n>       - Jump to line n
  :search <term>, :s      - Search for term
  :next, :n               - Next search match

\033[1mSelection:\033[0m
  :select <n>, :sel <n>   - Toggle select line n
  :copy                    - Copy selected lines

\033[1mEditing:\033[0m
  :edit, :e               - Open in vim/nano at cursor line
  :edit <n>               - Open in vim/nano at line n

\033[1mQuit:\033[0m
  :quit, :q               - Quit editor

Press Enter to continue..."""
        print(help_text)
        input()
    
    def run(self):
        """Main loop - command mode with preview"""
        if not HAS_TERMIOS:
            # Fallback: use input-based commands
            self.render()
            print("\n\033[90mCommand mode (input-based)\033[0m\n")
            
            while True:
                try:
                    cmd = input("\033[32m>\033[0m ").strip()
                    if not cmd:
                        self.render()
                        continue
                    
                    if cmd.lower() in ['q', 'quit', 'exit']:
                        break
                    
                    if cmd.startswith(':'):
                        result = self.execute_command(cmd[1:])
                    else:
                        # Try as line number
                        try:
                            line_num = int(cmd)
                            if self.jump_to_line(line_num):
                                self.render()
                                continue
                        except ValueError:
                            result = f'Unknown command: {cmd}'
                    
                    if result == 'quit':
                        break
                    elif result == 'help':
                        self.show_help()
                    elif result:
                        print(f"\033[33m{result}\033[0m")
                    
                    self.render()
                except (EOFError, KeyboardInterrupt):
                    break
            return
        
        # Use termios for arrow keys
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        
        try:
            new_settings = termios.tcgetattr(fd)
            new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)
            termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
            
            self.render()
            command_buffer = ''
            in_command_mode = False
            self._in_command_mode = False
            
            rows = get_terminal_size()[1]
            
            # Buffer for escape sequences
            escape_buffer = ''
            
            while True:
                if sys.stdin in select.select([sys.stdin], [], [], 0.01)[0]:
                    char = sys.stdin.read(1)
                    
                    if escape_buffer:
                        escape_buffer += char
                        if len(escape_buffer) >= 3 and escape_buffer[0] == '\x1b' and escape_buffer[1] == '[':
                            direction = escape_buffer[2]
                            escape_buffer = ''
                            
                            if direction == 'A':
                                self.move_up()
                                self.render()
                                continue
                            elif direction == 'B':
                                self.move_down()
                                self.render()
                                continue
                            elif direction == 'C':
                                self.move_right()
                                self.render()
                                continue
                            elif direction == 'D':
                                self.move_left()
                                self.render()
                                continue
                            elif direction == 'H':
                                self.cursor_col = 0
                                self._clamp_cursor()
                                self.render()
                                continue
                            elif direction == 'F':
                                self.cursor_col = len(self.lines[self.cursor_line])
                                self._clamp_cursor()
                                self.render()
                                continue
                        elif len(escape_buffer) > 3:
                            escape_buffer = ''
                        continue
                    
                    if in_command_mode:
                        if char == '\r' or char == '\n':
                            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                            
                            if command_buffer:
                                result = self.execute_command(command_buffer)
                                if result == 'quit':
                                    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
                                    break
                                elif result == 'help':
                                    self.show_help()
                                    new_settings = termios.tcgetattr(fd)
                                    new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)
                                    termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
                                    self.render()
                                elif result:
                                    print(f"\033[33m{result}\033[0m")
                                    import time
                                    time.sleep(1)
                            
                            command_buffer = ''
                            in_command_mode = False
                            self._in_command_mode = False
                            
                            new_settings = termios.tcgetattr(fd)
                            new_settings[3] = new_settings[3] & ~(termios.ECHO | termios.ICANON)
                            termios.tcsetattr(fd, termios.TCSADRAIN, new_settings)
                            self.render()
                        elif char == '\x1b':
                            command_buffer = ''
                            in_command_mode = False
                            self._in_command_mode = False
                            self.render()
                        elif char == '\x7f' or char == '\x08':
                            if command_buffer:
                                command_buffer = command_buffer[:-1]
                                rows = get_terminal_size()[1]
                                sys.stdout.write(f'\033[{rows};1H\033[2K')
                                sys.stdout.write(f'\033[1;36mCommand Mode\033[0m > :{command_buffer}')
                                sys.stdout.flush()
                        elif ord(char) >= 32 and ord(char) < 127:
                            command_buffer += char
                            rows = get_terminal_size()[1]
                            sys.stdout.write(f'\033[{rows};1H\033[2K')
                            sys.stdout.write(f'\033[1;36mCommand Mode\033[0m > :{command_buffer}')
                            sys.stdout.flush()
                    else:
                        if char == ':':
                            in_command_mode = True
                            self._in_command_mode = True
                            command_buffer = ''
                            sys.stdout.write(f'\033[{rows};1H\033[2K')
                            sys.stdout.write('\033[1;36mCommand Mode\033[0m > :')
                            sys.stdout.flush()
                        elif char == '\x1b':
                            escape_buffer = char
                            continue
                        elif char == '\r' or char == '\n':
                            line = self.lines[self.cursor_line]
                            before = line[:self.cursor_col]
                            after = line[self.cursor_col:]
                            self.lines[self.cursor_line] = before
                            self.lines.insert(self.cursor_line + 1, after)
                            self.cursor_line += 1
                            self.cursor_col = 0
                            self.render()
                        elif char == '\x7f' or char == '\x08':
                            self.delete_char_backward()
                            self.render()
                        elif char == 'q':
                            break
                        elif ord(char) == 3:
                            break
                        elif ord(char) >= 32 and ord(char) < 127:
                            self.insert_char(char)
                            self.render()
                else:
                    import time
                    time.sleep(0.01)
        
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            clear_screen()

