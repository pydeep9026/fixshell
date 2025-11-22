import re

def move_cursor_left(buffer, pos, word_boundary=False):
    if pos <= 0:
        return 0
    
    if word_boundary:
        return jump_to_word_start(buffer, pos)
    return pos - 1

def move_cursor_right(buffer, pos, word_boundary=False):
    if pos >= len(buffer):
        return len(buffer)
    
    if word_boundary:
        return jump_to_word_end(buffer, pos)
    return pos + 1

def jump_to_word_start(buffer, pos):
    if pos <= 0:
        return 0
    
    text_before = buffer[:pos]
    match = re.search(r'\S+\s*$', text_before)
    if match:
        return match.start()
    
    match = re.search(r'\w+$', text_before)
    if match:
        return match.start()
    
    while pos > 0 and buffer[pos - 1] == ' ':
        pos -= 1
    
    while pos > 0 and buffer[pos - 1] != ' ':
        pos -= 1
    
    return pos

def jump_to_word_end(buffer, pos):
    if pos >= len(buffer):
        return len(buffer)
    
    text_after = buffer[pos:]
    match = re.match(r'\S+', text_after)
    if match:
        return pos + match.end()
    
    match = re.match(r'\w+', text_after)
    if match:
        return pos + match.end()
    
    while pos < len(buffer) and buffer[pos] == ' ':
        pos += 1
    
    while pos < len(buffer) and buffer[pos] != ' ':
        pos += 1
    
    return pos

def get_word_at_cursor(buffer, pos):
    if pos < 0 or pos > len(buffer):
        return None, None, None
    
    start = pos
    end = pos
    
    while start > 0 and buffer[start - 1] not in [' ', '\t', '\n']:
        start -= 1
    
    while end < len(buffer) and buffer[end] not in [' ', '\t', '\n']:
        end += 1
    
    word = buffer[start:end]
    return word, start, end

def update_terminal_cursor(pos):
    print(f"\033[{pos}G", end='', flush=True)

def get_current_token(buffer, cursor_pos):
    word, start, end = get_word_at_cursor(buffer, cursor_pos)
    return word

def insert_text_at_cursor(buffer, cursor_pos, text):
    return buffer[:cursor_pos] + text + buffer[cursor_pos:], cursor_pos + len(text)

def delete_char_at_cursor(buffer, cursor_pos):
    if cursor_pos <= 0:
        return buffer, cursor_pos
    return buffer[:cursor_pos - 1] + buffer[cursor_pos:], cursor_pos - 1

def replace_word_at_cursor(buffer, cursor_pos, new_word):
    word, start, end = get_word_at_cursor(buffer, cursor_pos)
    if word is None:
        return buffer, cursor_pos
    
    new_buffer = buffer[:start] + new_word + buffer[end:]
    new_pos = start + len(new_word)
    return new_buffer, new_pos



