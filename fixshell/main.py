import sys
import os

from .command_loader import CommandLoader
from .command_suggester import CommandSuggester
from .shell_runner import ShellRunner
from .abbreviation_expander import AbbreviationExpander
from .snippet_manager import SnippetManager
from .danger_detector import DangerDetector
from .command_formatter import format_command
from .history_search import HistorySearch
from .session_recorder import SessionRecorder
from .env_detector import EnvDetector
from .theme_manager import ThemeManager
from .config_loader import ConfigLoader
from .completion_ui import CompletionUI
from .git_diff_viewer import GitDiffViewer
from .help_index_builder import HelpIndexBuilder
from .editor_with_commands import EditorWithCommands
from .utils import clear_screen, get_terminal_size

class FixShell:
    def __init__(self):
        self.config = ConfigLoader()
        self.command_loader = CommandLoader()
        self.command_suggester = CommandSuggester(self.command_loader)
        self.abbreviation_expander = AbbreviationExpander()
        self.snippet_manager = SnippetManager()
        self.danger_detector = DangerDetector()
        self.shell_runner = ShellRunner()
        self.history_search = HistorySearch()
        self.session_recorder = SessionRecorder(enabled=self.config.get("session_recording", True))
        self.env_detector = EnvDetector()
        self.theme_manager = ThemeManager()
        self.completion_ui = CompletionUI(self.command_loader)
        self.git_diff_viewer = GitDiffViewer()
        self.help_index_builder = HelpIndexBuilder()
        self.input_handler = None
        self.running = True
        
    def display_prompt(self):
        cols, rows = get_terminal_size()
        cwd = os.getcwd()
        home = os.path.expanduser('~')
        if cwd.startswith(home):
            cwd = '~' + cwd[len(home):]
        
        prompt = f"\033[32mfixshell\033[0m:\033[34m{cwd}\033[0m$ "
        return prompt
    
    def get_flag_description(self, buffer):
        tokens = buffer.split()
        if len(tokens) < 2:
            return None
        
        command_name = tokens[0]
        if command_name not in self.command_loader.commands_db:
            return None
        
        last_token = tokens[-1]
        if last_token.startswith('-'):
            subcommand = tokens[1] if len(tokens) > 1 and tokens[1] in self.command_loader.get_subcommands(command_name) else None
            desc = self.command_loader.get_flag_description(command_name, last_token, subcommand)
            return desc
        return None
    
    def get_flag_description_from_help(self, command):
        tokens = command.split()
        if len(tokens) < 2:
            return None
        
        command_name = tokens[0]
        last_token = tokens[-1]
        if last_token.startswith('-'):
            return self.help_index_builder.get_flag_description_from_help(command_name, last_token)
        return None
    
    def show_history_search(self):
        print("\nHistory Search (fuzzy):")
        print("Type a query to search history, or press Enter to cancel")
        try:
            query = input("> ").strip()
            if not query:
                return
            
            matches = self.history_search.search_history(query, limit=10)
            if matches:
                print(f"\nFound {len(matches)} matches:")
                for i, match in enumerate(matches, 1):
                    print(f"{i}. {match}")
                print("\nEnter number to use command, or press Enter to cancel:")
                try:
                    choice = input("> ").strip()
                    if choice.isdigit():
                        idx = int(choice) - 1
                        if 0 <= idx < len(matches):
                            print(f"Using: {matches[idx]}\n")
                            return matches[idx]
                except (EOFError, KeyboardInterrupt):
                    print()
            else:
                print("No matches found")
        except (EOFError, KeyboardInterrupt):
            print()
        return None
    
    def handle_save_snippet(self, user_input):
        parts = user_input.split(' ', 2)
        if len(parts) < 3:
            print("Usage: /save <name> <template>")
            print("Example: /save build \"docker build -t {name} .\"")
            return
        
        name = parts[1]
        template = parts[2]
        self.snippet_manager.save_snippet(name, template)
        print(f"\033[32m✓ Snippet '{name}' saved!\033[0m")
    
    def show_time(self):
        from datetime import datetime, timezone, timedelta
        
        utc_now = datetime.now(timezone.utc)
        
        ist_offset = timedelta(hours=5, minutes=30)
        cst_offset = timedelta(hours=-6)
        
        ist_time = utc_now + ist_offset
        cst_time = utc_now + cst_offset
        utc_time = utc_now
        
        print("\n\033[1mCurrent Time:\033[0m")
        print(f"  \033[36mIST\033[0m  (India Standard Time):     {ist_time.strftime('%A, %Y-%m-%d %H:%M:%S')} (UTC+5:30)")
        print(f"  \033[33mCST\033[0m  (Chicago Standard Time):   {cst_time.strftime('%A, %Y-%m-%d %H:%M:%S')} (UTC-6:00)")
        print(f"  \033[32mUTC\033[0m  (Coordinated Universal):   {utc_time.strftime('%A, %Y-%m-%d %H:%M:%S')}")
        print(f"  \033[32mGMT\033[0m  (Greenwich Mean Time):    {utc_time.strftime('%A, %Y-%m-%d %H:%M:%S')}")
        print()
    
    def show_help(self):
        print("\n\033[1mfixshell Commands:\033[0m")
        print("  /edit <file>[:line], /e <file>[:line] - Open editor for file")
        print("    Example: /edit test.py:5 (opens at line 5)")
        print("  /history, /h      - Search command history (fuzzy)")
        print("  /save <name> <template> - Save a command snippet")
        print("  /time             - Show current time (IST, CST, UTC, GMT)")
        print("  /help, /?         - Show this help")
        print("  exit              - Exit fixshell")
        print("\n\033[1mFeatures:\033[0m")
        print("  • Typo detection and correction")
        print("  • Auto-completion suggestions")
        print("  • Abbreviation expansion (kgp, kga, etc.)")
        print("  • Command snippets")
        print("  • Danger detection for destructive commands")
        print("  • Auto-group flags (-a -l -h → -alh)")
        print("  • Inline flag descriptions")
        print("  • Git diff viewer (colorized)")
        print("  • Command timer (for commands > 10s)")
        print("  • Session recording")
        print("  • Environment detection (Python venv)")
        print("  • History search")
        print()

    
    def display_flag_help(self, buffer):
        desc = self.get_flag_description(buffer)
        if desc:
            last_token = buffer.split()[-1] if buffer.split() else ''
            sys.stdout.write(f'\n\033[36m{last_token} → {desc}\033[0m')
            sys.stdout.flush()
    
    def process_input(self, buffer):
        expanded, changed = self.abbreviation_expander.expand_abbreviation(buffer)
        if changed:
            buffer = expanded
        
        expanded, changed = self.snippet_manager.expand_input(buffer)
        if changed:
            buffer = expanded
        
        buffer = format_command(buffer)
        
        return buffer
    
    def should_show_timer(self, execution_time):
        return execution_time > 10.0
    
    def run_shell_loop(self):
        clear_screen()
        print("\033[1m\033[32mfixshell\033[0m - Smart Terminal Wrapper")
        print("Type 'exit' to quit or '/help' for commands")
        
        features_enabled = []
        if self.config.get("show_suggestions", True):
            features_enabled.append("typo detection")
        if self.config.get("show_completions", True):
            features_enabled.append("auto-completion")
        if self.config.get("danger_detection", True):
            features_enabled.append("danger detection")
        if self.config.get("session_recording", True):
            features_enabled.append("session recording")
        if self.config.get("git_diff_viewer", True):
            features_enabled.append("git diff viewer")
        
        if features_enabled:
            print(f"\033[90mFeatures: {', '.join(features_enabled)}\033[0m")
        print()
        
        self.session_recorder.start_session()
        
        try:
            while self.running:
                try:
                    prompt = self.display_prompt()
                    user_input = input(prompt).strip()
                except (EOFError, KeyboardInterrupt):
                    print("\n")
                    self.running = False
                    break
                
                if user_input.startswith('/'):
                    user_input_lower = user_input.lower()
                    if user_input_lower == '/time':
                        self.show_time()
                        continue
                    elif user_input_lower.startswith('/edit ') or user_input_lower.startswith('/e '):
                        parts = user_input.split(' ', 1)
                        if len(parts) < 2:
                            print("Usage: /edit <file>[:line] or /e <file>[:line]")
                            print("Example: /edit test.py:5")
                            print()
                            continue
                        
                        file_spec = parts[1].strip()
                        line_num = None
                        search_term = None
                        
                        if ':' in file_spec:
                            file_path, location = file_spec.rsplit(':', 1)
                            if location.isdigit():
                                line_num = int(location)
                            else:
                                search_term = location
                        else:
                            file_path = file_spec
                        
                        if not file_path:
                            print("Usage: /edit <file>[:line] or /e <file>[:line]")
                            print()
                            continue
                        
                        if not os.path.isabs(file_path):
                            file_path = os.path.join(os.getcwd(), file_path)
                        
                        try:
                            editor = EditorWithCommands(file_path)
                            if line_num:
                                editor.jump_to_line(line_num)
                            editor.run()
                        except Exception as e:
                            print(f"\033[31mError opening editor: {str(e)}\033[0m")
                            import traceback
                            traceback.print_exc()
                        print()
                        continue
                    elif user_input_lower == '/history' or user_input_lower == '/h':
                        result = self.show_history_search()
                        if result:
                            user_input = result
                        else:
                            continue
                    elif user_input_lower.startswith('/save '):
                        self.handle_save_snippet(user_input)
                        print()
                        continue
                    elif user_input_lower == '/help' or user_input_lower == '/?' or user_input_lower == '/commands':
                        self.show_help()
                        continue
                
                if not user_input:
                    continue
                
                command = user_input
                
                if command == 'exit':
                    self.running = False
                    break
                
                # Handle cd command specially - change directory in current process
                if command.startswith('cd '):
                    parts = command.split(None, 1)
                    if len(parts) == 1:
                        # cd without arguments - go to home
                        try:
                            os.chdir(os.path.expanduser('~'))
                        except Exception as e:
                            print(f"\033[31mError: {str(e)}\033[0m\n")
                        continue
                    else:
                        target_dir = parts[1].strip()
                        # Expand ~ and handle relative paths
                        if target_dir.startswith('~'):
                            target_dir = os.path.expanduser(target_dir)
                        elif not os.path.isabs(target_dir):
                            target_dir = os.path.join(os.getcwd(), target_dir)
                        try:
                            os.chdir(target_dir)
                        except Exception as e:
                            print(f"\033[31mError: {str(e)}\033[0m\n")
                        continue
                
                completions = self.completion_ui.get_completions(command)
                if completions and len(completions) > 0 and self.config.get("show_completions", True):
                    print(f"\033[90m💡 Completions: {', '.join(completions[:5])}\033[0m")
                
                suggestion = self.command_suggester.suggest_correction(command)
                if suggestion:
                    print(f"\033[33m→ Did you mean: {suggestion['suggestion']}? (y/n)\033[0m", end=' ')
                    try:
                        confirm = input().strip().lower()
                        if confirm == 'y':
                            tokens = command.split()
                            if suggestion['position'] < len(tokens):
                                tokens[suggestion['position']] = suggestion['suggestion']
                                command = ' '.join(tokens)
                                print(f"\033[32mUsing: {command}\033[0m")
                    except (EOFError, KeyboardInterrupt):
                        print()
                        continue
                
                flag_desc = self.get_flag_description(command)
                if not flag_desc:
                    flag_desc = self.get_flag_description_from_help(command)
                if flag_desc:
                    last_token = command.split()[-1] if command.split() else ''
                    if last_token.startswith('-'):
                        print(f"\033[36m📖 {last_token} → {flag_desc}\033[0m")
                
                command = self.process_input(command)
                
                danger_info = self.danger_detector.check_danger(command)
                if danger_info:
                    self.danger_detector.show_danger_warning(command, danger_info)
                    try:
                        confirm = input().strip().lower()
                        if confirm != 'y':
                            print("Command cancelled.\n")
                            continue
                    except (EOFError, KeyboardInterrupt):
                        print("\nCommand cancelled.\n")
                        continue
                
                if self.env_detector.should_prompt():
                    venv_path = self.env_detector.find_venv_path()
                    if venv_path:
                        self.env_detector.prompt_activate_venv(venv_path)
                        try:
                            confirm = input().strip().lower()
                            if confirm == 'y':
                                activate_script = os.path.join(venv_path, 'bin', 'activate')
                                if os.path.exists(activate_script):
                                    print(f"Run: source {activate_script}\n")
                        except (EOFError, KeyboardInterrupt):
                            print()
                
                output, return_code, execution_time = self.shell_runner.execute_command(command)
                
                if output:
                    if self.git_diff_viewer.is_git_diff_command(command):
                        formatted_output = self.git_diff_viewer.display_diff(output)
                        print(formatted_output)
                    else:
                        print(output)
                
                if self.should_show_timer(execution_time):
                    print(f"\033[90m({execution_time:.2f}s)\033[0m")
                
                success = return_code == 0
                self.session_recorder.log_command(command, success)
                self.history_search.add_to_history(command)
                print()
        
        except KeyboardInterrupt:
            print("\n\nExiting...")
        finally:
            self.session_recorder.end_session()
            print("Goodbye!")

def main():
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == '--version':
        print('fixshell 0.1.0')
        return
    
    shell = FixShell()
    shell.run_shell_loop()

if __name__ == '__main__':
    main()

