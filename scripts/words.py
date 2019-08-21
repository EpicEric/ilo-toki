import functools
import re

import jan_pije


OFFICIAL_WORD_LIST = sorted(functools.reduce(lambda x, y: x + y, jan_pije.NEW_WORDS_PER_LESSON.values()))
EXTINCT_WORD_LIST = ['apeja', 'kijetesantakalu', 'kipisi', 'leko', 'monsuta', 'po', 'tuli']
FULL_WORD_LIST = sorted(OFFICIAL_WORD_LIST + EXTINCT_WORD_LIST)

REGEX_EXTINCT_WORDS = r'\b({})\b'.format('|'.join(EXTINCT_WORD_LIST))


def has_extinct_words(sentence):
    return bool(re.search(REGEX_EXTINCT_WORDS, sentence))
