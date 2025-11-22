# fixshell Setup for GCP Cloud Workstation

## Quick Setup (3 Steps)

```bash
# 1. Clone the repository
git clone <repo-url>
cd fixshell

# 2. Run setup script
chmod +x setup.sh
./setup.sh

# 3. Reload shell
source ~/.bashrc

# Done! Now use fixshell
fixshell
```

## What the Setup Script Does

1. Installs fixshell to `~/.local/fixshell`
2. Creates `~/.local/bin/fixshell` command
3. Adds `~/.local/bin` to your PATH in `~/.bashrc`
4. Makes everything executable

## Verify Installation

```bash
fixshell --version
# Should output: fixshell 0.1.0
```

## After Setup

Just type `fixshell` from anywhere to start using it!

```bash
fixshell
```

## Troubleshooting

**If `fixshell` command not found:**
```bash
# Make sure PATH is updated
source ~/.bashrc

# Or manually add to PATH
export PATH="$HOME/.local/bin:$PATH"

# Verify fixshell exists
ls ~/.local/bin/fixshell
```

**If import errors:**
```bash
# Check installation
ls -la ~/.local/fixshell/fixshell/

# Re-run setup
./setup.sh
```

## Uninstall

```bash
rm -rf ~/.local/fixshell
rm ~/.local/bin/fixshell
# Remove PATH line from ~/.bashrc
```

That's it! Simple and clean for cloud workstations.

