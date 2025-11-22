# fixshell

A local Python smart terminal wrapper for GCP Cloud Workstations. Enhances command-line editing with typo correction, auto-completion, and smart features - all running locally, no AI required.

## Features

- **Typo Detection** - Detects and suggests corrections for typos
- **Auto-Completion** - Shows completion suggestions as you type
- **Abbreviation Expansion** - Pre-defined SRE kubectl aliases (kgp, kga, etc.)
- **Command Snippets** - Save and reuse command templates
- **Danger Detection** - Warns before destructive commands
- **Auto-Group Flags** - Combines short flags automatically
- **Flag Descriptions** - Shows flag descriptions inline
- **Git Diff Viewer** - Colorized git diff output
- **Command Timer** - Shows execution time for slow commands
- **Session Recording** - Logs commands to session files
- **History Search** - Fuzzy search through command history
- **Environment Detection** - Detects Python projects and suggests venv activation

## Installation (GCP Cloud Workstation)

### Quick Install

```bash
# Clone the repository
git clone <repo-url>
cd fixshell

# Run setup script
chmod +x setup.sh
./setup.sh

# Reload shell
source ~/.bashrc

# Start using fixshell
fixshell
```

That's it! The setup script will:
- Install fixshell to `~/.local/fixshell`
- Add `~/.local/bin` to your PATH
- Create the `fixshell` command

### Verify Installation

```bash
fixshell --version
```

Should output: `fixshell 0.1.0`

## Usage

Simply type `fixshell` to start:

```bash
fixshell
```

### Built-in Commands

- `:help` or `:?` - Show help
- `:history` or `:h` - Search command history (fuzzy)
- `:save <name> <template>` - Save a command snippet
- `exit` - Exit fixshell

## Examples

### Typo Detection
```bash
fixshell> git psuh
→ Did you mean: push? (y/n) y
```

### Abbreviation Expansion
```bash
fixshell> kgp
# Automatically expands to: kubectl get pods
```

### Command Snippets
```bash
fixshell> :save deploy "kubectl apply -f {file} -n {namespace}"
✓ Snippet 'deploy' saved!

fixshell> deploy app.yaml production
# Expands to: kubectl apply -f app.yaml -n production
```

### History Search
```bash
fixshell> :history
> git po
Found 3 matches:
  1. git push origin main
  2. git pull origin develop
  # Select by number
```

### Auto-Completion
```bash
fixshell> docker ru
💡 Completions: run, rmi, restart
```

### Flag Descriptions
```bash
fixshell> kubectl get -n
📖 -n → Namespace
```

## Configuration

Edit `~/.local/fixshell/data/config.json` to enable/disable features:

```json
{
  "show_suggestions": true,
  "show_completions": true,
  "danger_detection": true,
  "session_recording": true,
  "command_timer": true,
  "flag_descriptions": true,
  "git_diff_viewer": true
}
```

## Project Structure

```
fixshell/
├── fixshell/              # Main package
│   ├── main.py           # Entry point
│   ├── command_loader.py # Loads command database
│   ├── command_suggester.py # Typo detection
│   └── ...               # Other modules
├── data/                 # Configuration files
│   ├── commands.json     # Command database
│   ├── abbreviations.json # SRE kubectl aliases
│   └── config.json       # Settings
├── themes/               # Theme files
├── setup.sh              # Installation script
└── fixshell_launcher.py  # Launcher script
```

## Requirements

- Python 3.6+ (pre-installed on Cloud Workstations)
- Bash shell
- No external dependencies (uses only Python standard library)
- No internet connection required after installation

## Uninstall

```bash
rm -rf ~/.local/fixshell
rm ~/.local/bin/fixshell
# Remove PATH line from ~/.bashrc or ~/.zshrc
```

## License

MIT
