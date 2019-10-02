# -*- coding: utf-8 -*-
import re

def escape_inline(s):
    return re.sub(r'([\{\}<>\|%\*;\#\$\\\@`])', r'\\\1', s)

class InlineText:
    def __init__(self, text):
        self.val = text 

def inlinetext_from_str(text):
    return InlineText(text)

class Option:
    def __init__(self, val):
        self.val = val

def option(val):
    return Option(val)

def convert(x):
    t = type(x)
    if t is int:
        return convert_int(x)
    elif t is str:
        return convert_str(x)
    elif t is InlineText:
        return convert_inlinetext(x)
    elif t is Option:
        return convert_option(x)
    elif t is list:
        return convert_list(x)
    elif t is tuple:
        return convert_tuple(x)
    elif t is dict:
        return convert_dict(x, x.keys())
    else:
        return 'None'

def convert_int(x):
    if x is None:
        return None
    else:
        return str(x)

def convert_str(x):
    if x is None:
        return None
    else:
        for i in range(4,0,-1):
            if '`' * i in x:
                return ('`' * (i+1)) + str(x) + ('`' * (i+1))
        return '`' + str(x) + '`'

def convert_inlinetext(x):
    if x.val is None:
        return None
    return '{' + escape_inline(x.val) + '}'

def convert_option(x):
    if x.val is None:
        return 'None'
    else:
        return 'Some(' + convert(x.val) + ')'


def convert_list(x):
    result = '['
    for item in x:
        result += convert(item)
        result += "; "
    result = result[0:-2]
    result += ']'
    return result

def convert_tuple(x):
    result = '('
    for item in x:
        result += convert(item)
        result += ", "
    result = result[0:-2]
    result += ')'
    return result

def convert_dict(x, keys, indent = '    '):
    result = '(|\n'
    for key in keys:
        result += indent
        result += str(key) + ' = '
        result += convert(x[key]) + ';\n'
    result = result[0:-2]
    result += '\n|)'
    return result
