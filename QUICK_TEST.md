# fixshell - Quick Test Guide

Test all features with these commands:

## 1. Start fixshell
```bash
fixshell
```

## 2. Typo Detection
```bash
fixshell> git psuh
# Should suggest: push

fixshell> kubectl ge pods
# Should suggest: get

fixshell> docker ru
# Should suggest: run
```

## 3. Abbreviation Expansion (SRE Aliases)
```bash
fixshell> kgp
# Expands to: kubectl get pods

fixshell> kga
# Expands to: kubectl get all

fixshell> kl
# Expands to: kubectl logs

fixshell> kex pod-name -- sh
# Expands to: kubectl exec -it pod-name -- sh
```

## 4. Command Snippets
```bash
fixshell> /save build "docker build -t {name} ."
# Saves snippet

fixshell> build myapp
# Expands to: docker build -t myapp .

fixshell> /save deploy "kubectl apply -f {file} -n {namespace}"
fixshell> deploy app.yaml production
# Expands to: kubectl apply -f app.yaml -n production

## 5. History Search
```bash
fixshell> /history
> git
# Shows matching past commands

fixshell> /h
> kubectl
# Fuzzy search through history
```

## 6. Auto-Completion
```bash
fixshell> docker ru
# Shows: 💡 Completions: run, rmi, restart

fixshell> git pu
# Shows: 💡 Completions: push, pull

fixshell> kubectl ge
# Shows: 💡 Completions: get, get
```

## 7. Flag Descriptions
```bash
fixshell> kubectl get -n
# Shows: 📖 -n → Namespace

fixshell> git commit --amend
# Shows: 📖 --amend → Amend the previous commit

fixshell> docker run -d
# Shows: 📖 -d → Run in background
```

## 8. Danger Detection
```bash
fixshell> rm -rf /
# Shows: ⚠️  This command is destructive — Delete root filesystem
# Requires confirmation

fixshell> git reset --hard
# Shows warning and requires confirmation

fixshell> kubectl delete pod --all
# Shows warning and requires confirmation
```

## 9. Auto-Group Flags
```bash
fixshell> ls -a -l -h
# Auto-formats to: ls -alh

fixshell> docker ps -a -l
# Auto-formats to: docker ps -al
```

## 10. Git Diff Viewer
```bash
fixshell> git diff
# Shows colorized diff output

fixshell> git show HEAD
# Shows colorized output

fixshell> git log -p
# Shows colorized patch output
```

## 11. Command Timer
```bash
fixshell> sleep 11
# Shows: (11.0s) after execution

fixshell> find / -name "*.log" 2>/dev/null
# Shows execution time if > 10 seconds
```

## 12. Environment Detection
```bash
# In a Python project directory
fixshell> python script.py
# Detects if venv is not activated and prompts

fixshell> cd /path/to/python/project
fixshell> pytest
# Prompts to activate venv if not activated
```

## 13. Session Recording
```bash
# Run any commands
fixshell> git status
fixshell> ls -la
fixshell> echo "test"

# Check session log
cat ~/.local/fixshell/sessions/session_*.log
# Shows: timestamp ✓ command
```

## 14. Help Command
```bash
fixshell> /help
# Shows all available commands and features

fixshell> /?
# Same as /help
```

## 15. Built-in Commands
```bash
fixshell> /time
# Show current time in IST, CST, UTC, GMT (with day of week)

fixshell> /save test "echo {name}"
# Save snippet

fixshell> /history
# Search history

fixshell> /help
# Show help

fixshell> exit
# Exit fixshell
```

## Complete Test Flow

```bash
# 1. Start fixshell
fixshell

# 2. Test typo
git psuh
# Answer: y

# 3. Test abbreviation
kgp

# 4. Test snippet
/save hello "echo Hello {name}!"
hello World

# 5. Test history
/history
# Type: git

# 6. Test completion
docker ru

# 7. Test flag description
kubectl get -n

# 8. Test danger (cancel it)
rm -rf /
# Answer: n

# 9. Test normal command
echo "fixshell works!"

# 10. Exit
exit
```

All features should work as expected!

