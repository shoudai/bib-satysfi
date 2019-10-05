import bibtexparser
import textwrap
import re
import pysaty

def author(item):
    item = bibtexparser.customization.author(item)
    authors = []
    for author in item['author']:
        if author == 'others, ':
            authors.append('et al.')
            break
        try:
            name = bibtexparser.customization.splitname(author)
        except bibtexparser.customization.InvalidName:
            return [author[0:-2]]
        
        result = ''
        for first in name['first']:
            for i, fst in enumerate(first.split('-')):
                if i > 0:
                    result += '-'
                result += fst[0] + '.'
            result += ' '
        if name['von'] != []:
            result += name['von'][0] + ' '
        result += name['last'][0]
        authors.append(result)
    return authors

def page(pages):
    results = ""
    for i, page in enumerate(pages.split('--')):
        if i > 0:
            results += '–'
        results += page
    return pysaty.inlinetext_from_str(results)

def strs_to_ints(keys, x):
    for key in keys:
        x[key] = int(x[key])
    return x

def strs_to_inlines(keys, x):
    for key in keys:
        try:
            x[key] = pysaty.inlinetext_from_str(x[key])
        except:
            x[key] = None
    return x

def to_options(keys, x):
    for key in keys:
        try:
            x[key] = pysaty.option(x[key])
        except:
            x[key] = pysaty.option(None)
    return x

with open('references.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

saty = """@import: bib-style

let bibliography = [
"""

for item in bib_database.entries:
    if item['ENTRYTYPE'] == 'inproceedings':
        saty += '(`' + item['ID'] + '`, InProceedings'
        item['pages'] = page(item['pages'])
        int_keys = ['volume', 'year']
        inline_keys = ['title', 'booktitle', 'number', 'organization']
        option_keys = []
        keys = ['author', 'title', 'booktitle', 'volume', 'number', 'pages', 'organization', 'year']
    
    elif item['ENTRYTYPE'] == 'article':
        saty += '(`' + item['ID'] + '`, Article'
        item['pages'] = page(item['pages'])
        int_keys = ['volume', 'year']
        inline_keys = ['title', 'journal', 'number', 'publisher']
        option_keys = ['number', 'publisher', 'url']
        keys = ['author', 'title', 'journal', 'volume', 'number', 'pages', 'year', 'publisher', 'url']

    elif item['ENTRYTYPE'] == 'book':
        saty += '(`' + item['ID'] + '`, Book'
        int_keys = ['year']
        inline_keys = ['title', 'chapter', 'publisher']
        option_keys = ['chapter']
        keys = ['author', 'title', 'chapter', 'publisher', 'year']

    elif item['ENTRYTYPE'] == 'phdthesis' or item['ENTRYTYPE'] == 'mastersthesis':
        saty += '(`' + item['ID'] + '`, Thesis'
        int_keys = ['year']
        item['degree'] = 'Ph.D. thesis' if item['ENTRYTYPE'] == 'phdthesis' else 'Masters thesis'
        inline_keys = ['title', 'degree', 'school']
        option_keys = []
        keys = ['author', 'title', 'degree', 'school', 'year']
    
    item['author'] = author(item)
    item = strs_to_ints(int_keys, item)
    item = strs_to_inlines(inline_keys, item)
    item = to_options(option_keys, item)
    saty += pysaty.convert_dict(item, keys) + ');\n\n'

saty += "]"

with open('../bib-content.satyh', mode='w') as saty_file:
    saty_file.write(saty)