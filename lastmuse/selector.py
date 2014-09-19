# This module contains functions to help with video selection     

def select(original, names):
    try:
        keywords = open("lastmuse/_keywords_", "r")
    except IOError: # If the file does not exist
        return _length_test(original, names)

    return _keywords_test(keywords, names, original)

def _length_test(orig, options):
    
    l_orig = len(orig)
    options_length = []

    for option in options:
        options_length.append(len(option))

    for i in range(len(options_length)):
        options_length[i] -= l_orig
        options_length[i] = abs(options_length[i])
        
    return sorted(options_length)[0]

def _keywords_test(keywords, options, original):
    
    names = list(options)
    lines = _get_lines(keywords)
    
    for name in names:
        if original.lower() not in name.lower():
            names.remove(name)

    for line in lines:

        if line[0] == '+':
            names = _apply_positive(line[1:], names)
        elif line[0] == '-':
            names = _apply_negative(line[1:], names)
        
        if len(names) == 1:
            return names[0]

    return names[0]

def _get_lines(file_):

    raw = file_.read()
    lines = raw.split('\n')

    for i in range(lines.count('')):
        lines.remove('')
    
    return lines

def _apply_positive(word, opts):
    
    names = list(opts)
    for name in names:
        if word.lower() not in name.lower():
            names.remove(name)

    return names
def _apply_negative(word, opts):

    names = list(opts)
    for name in names:
        if word.lower() in name.lower():
            names.remove(name)

    return names
