import re

def detect_short_flags(tokens):
    flag_groups = []
    current_group = []
    start_idx = None
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if token.startswith('-') and not token.startswith('--') and len(token) == 2:
            if start_idx is None:
                start_idx = i
            current_group.append(token)
        else:
            if len(current_group) > 1:
                flag_groups.append((start_idx, current_group))
            current_group = []
            start_idx = None
        i += 1
    
    if len(current_group) > 1:
        flag_groups.append((start_idx, current_group))
    
    return flag_groups

def group_flags(command):
    tokens = command.split()
    if len(tokens) < 3:
        return command
    
    flag_groups = detect_short_flags(tokens)
    
    if not flag_groups:
        return command
    
    processed = set()
    result_tokens = []
    
    for start_idx, flags in flag_groups:
        for idx in range(start_idx, start_idx + len(flags)):
            processed.add(idx)
        combined = '-' + ''.join([f[1] for f in flags])
        result_tokens.append((start_idx, combined))
    
    for i, token in enumerate(tokens):
        if i not in processed:
            result_tokens.append((i, token))
    
    result_tokens.sort(key=lambda x: x[0])
    return ' '.join([token for _, token in result_tokens])

def align_arguments(command):
    lines = command.split('\n')
    if len(lines) == 1:
        tokens = command.split()
        if len(tokens) <= 5:
            return command
        
        formatted_lines = []
        current_line = []
        indent = 0
        
        for token in tokens:
            if token.startswith('--') and current_line:
                formatted_lines.append(' '.join(current_line))
                current_line = [token]
            else:
                current_line.append(token)
                if len(' '.join(current_line)) > 80 and len(current_line) > 1:
                    formatted_lines.append(' '.join(current_line[:-1]))
                    current_line = [current_line[-1]]
        
        if current_line:
            formatted_lines.append(' '.join(current_line))
        
        return ' \\\n  '.join(formatted_lines) if len(formatted_lines) > 1 else command
    
    return command

def format_command(command):
    if not command or not command.strip():
        return command
    
    formatted = group_flags(command)
    formatted = align_arguments(formatted)
    return formatted

