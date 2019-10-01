import bibtexparser
import textwrap
import re

def escape_inline(s):
    return re.sub(r'([\{\}<>\|%\*;\#\$\\\@`])', r'\\\1', s)

def option(item, key):
    return 'Some({' + item[key] + '})' if key in item else 'None'

def option_str(item, key):
    return 'Some(`' + item[key] + '`)' if key in item else 'None'
def author_str(item):
    item = bibtexparser.customization.author(item)
    results = ' '
    for author in item['author']:
        if author == 'others, ':
            results += '`et al.` ; '
            break
        results += '`'
        name = bibtexparser.customization.splitname(author)
        for first in name['first']:
            for i, fst in enumerate(first.split('-')):
                if i > 0:
                    results += '-'
                results += fst[0] + '.'
            results += ' '
        if name['von'] != []:
            results += name["von"] + ' '
        results += name['last'][0] + '` ; '
    return results[0:-2]

def page_str(pages):
    results = ""
    for i, page in enumerate(pages.split('--')):
        if i > 0:
            results += '–'
        results += page
    return results

with open('references.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

saty = """@import: bib

let bibliography = ["""

for item in bib_database.entries:
    if item['ENTRYTYPE'] == 'inproceedings':
        item['author'] = author_str(item)
        item['pages'] = page_str(item['pages'])
        saty += textwrap.dedent("""
            (`{ID}`, InProceedings(|
            author = [{author}];
            title = {{{title}}};
            booktitle = {{{booktitle}}};
            volume = {volume};
            number = {{{number}}};
            pages = {{{pages}}};
            organization = {{{organization}}};
            year = {year};
            |));
        """.format(**item))

    elif item['ENTRYTYPE'] == 'article':
        item['author'] = author_str(item)
        item['title'] = escape_inline(item['title'])
        item['pages'] = page_str(item['pages'])
        item['number'] = option(item, 'number')
        item['publisher'] = option(item, 'publisher')
        item['url'] = option_str(item, 'url')
        saty += textwrap.dedent("""
            (`{ID}`, Article(|
            author = [{author}];
            title = {{{title}}};
            journal = {{{journal}}};
            volume = {volume};
            number = {number};
            pages = {{{pages}}};
            year = {year};
            publisher = {publisher};
            url       = {url};
            |));
        """.format(**item))

    elif item['ENTRYTYPE'] == 'book':
        item['author'] = author_str(item)
        item['chapter'] = option(item, 'chapter')
        saty += textwrap.dedent("""
            (`{ID}`, Book(|
            author = [{author}];
            title = {{{title}}};
            chapter = {chapter};
            year = {year};
            publisher = {{{publisher}}};
            |));
        """.format(**item))

    elif item['ENTRYTYPE'] == 'phdthesis' or item['ENTRYTYPE'] == 'mastersthesis':
        item['author'] = author_str(item)
        item['degree'] = 'Ph.D. thesis' if item['ENTRYTYPE'] == 'phdthesis' else 'Masters thesis'
        saty += textwrap.dedent("""
            (`{ID}`, Thesis(|
            author = [{author}];
            title = {{{title}}};
            degree = {{{degree}}};
            school = {{{school}}};
            year = {year};
            |));
        """.format(**item))

saty += "]"

with open('../bib-content.satyh', mode='w') as saty_file:
    saty_file.write(saty)