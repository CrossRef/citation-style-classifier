STYLES = [
    'acm-sig-proceedings',
    'american-chemical-society',
    'american-chemical-society-with-titles',
    'american-institute-of-physics',
    'american-sociological-association',
    'apa',
    'bmc-bioinformatics',
    'chicago-author-date',
    'elsevier-without-titles',
    'elsevier-with-titles',
    'harvard3',
    'ieee',
    'iso690-author-date-en',
    'modern-language-association',
    'springer-basic-author-date',
    'springer-lecture-notes-in-computer-science',
    'vancouver']


MIN_REF_LEN = 11

REGEX_REMOVE = ['Retrieved$', 'Available from:$', '\[Internet\]',
                '\[online\]',  'doi:$']

REGEX_RANDOM_REMOVE = ['^\(1\)', '^\[1\]', '^1\.', '^1(?!\d)', '\.$']

YEAR_PATTERN = '(?:16|17|18|19|20)\d{2}'

MONTH_ABBR_PATTERN = '(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'

MONTH_PATTERN = '(?:January|February|March|April|May|June|July|August|' + \
                'September|October|November|December)'

REGEX_MONTH_REMOVE = {
    r'\('+MONTH_ABBR_PATTERN+'\. ('+YEAR_PATTERN+')\)': r'(\1)',
    r'(?<![a-zA-Z])'+MONTH_ABBR_PATTERN+'\. ('+YEAR_PATTERN+')\.': r'\1.',
    r'(?<!\d)('+YEAR_PATTERN+') '+MONTH_ABBR_PATTERN+';': r'\1;',
    r'\('+MONTH_PATTERN+'\)': '',
    r'\('+MONTH_PATTERN+' [123]?\d\)': '',
    r'(?<![a-zA-Z])'+MONTH_PATTERN+' ('+YEAR_PATTERN+')\.': r'\1.',
    r'(?<!\d)[123]?\d\ '+MONTH_PATTERN+' ('+YEAR_PATTERN+')\.': r'\1.'}


REGEX_WORD_TO_TOKEN = {
    '(?<![a-zA-Z])[a-z]{2,}(?![a-zA-Z])': 'lcword',
    '(?<![a-zA-Z])[a-z](?![a-zA-Z])': 'lclett',
    '(?<![a-zA-Z])[A-Z]{2,}(?![a-zA-Z])': 'ucword',
    '(?<![a-zA-Z])[A-Z](?![a-zA-Z])': 'uclett',
    '(?<![a-zA-Z])[A-Z][a-z]+(?![a-zA-Z])': 'capword',
    '[A-Za-z]*[A-Z][A-Za-z]*': 'word',
    '(?<!\d)'+YEAR_PATTERN+'(?!\d)': 'year',
    '(?<!\d)\d+(?!\d)': 'num',
    '\.': 'dot',
    ',': 'comma',
    '\(': 'lpar',
    '\)': 'rpar',
    '\[': 'lbracket',
    '\]': 'rbracket',
    ':': 'colon',
    ';': 'semicolon',
    '/': 'slash',
    '&': 'and',
    '[\u002D\u00AD\u2010\u2011\u2012\u2013\u2014\u2015\u207B' +
    '\u208B\u2212-]': 'dash',
    '[“”]': 'quot',
    '[^a-z ]+': 'other'}

NGRAM_RANGE = (1, 2)
