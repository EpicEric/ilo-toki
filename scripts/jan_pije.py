import re

NEW_WORDS_PER_LESSON = {
    3: ['jan', 'mi', 'moku', 'sina', 'suli', 'suno', 'telo', 'pona', 'li'],
    4: ['ilo', 'kili', 'ni', 'ona', 'pipi', 'ma', 'ijo', 'jo', 'lukin', 'pakala', 'unpa', 'wile', 'e'],
    5: ['ike', 'jaki', 'lawa', 'len', 'lili', 'mute', 'nasa', 'seli', 'sewi', 'tomo', 'utala'],
    6: ['kama', 'kepeken', 'kiwen', 'kon', 'lon', 'pana', 'poki', 'toki', 'tawa'],
    7: ['anpa', 'insa', 'monsi', 'sama', 'tan', 'poka'],
    8: ['ala', 'ale', 'ali', 'ken', 'lape', 'musi', 'pali', 'sona', 'wawa'],
    9: ['a', 'awen', 'mama', 'mije', 'meli', 'mu', 'nimi', 'o'],
    10: ['olin', 'seme', 'sin', 'supa', 'suwi'],
    11: ['pi', 'kalama', 'kulupu', 'nasin'],
    12: ['ante', 'anu', 'en', 'kin', 'lete', 'lipu', 'mani', 'pilin', 'taso'],
    13: ['jelo', 'kule', 'laso', 'loje', 'pimeja', 'sitelen', 'walo'],
    14: ['akesi', 'kala', 'kasi', 'moli', 'soweli', 'waso'],
    15: ['ko', 'kute', 'linja', 'luka', 'lupa', 'nena', 'noka', 'oko', 'palisa', 'selo', 'sijelo', 'sike', 'sinpin', 'uta'],
    16: ['nanpa', 'tu', 'wan', 'weka'],
    17: ['la', 'mun', 'tenpo', 'open', 'pini'],
    18: ['alasa', 'namako', 'pu', 'esun', 'pan']
}

REGEX_LIST = None


def get_lesson_for_sentence(sentence):
    global REGEX_LIST
    if not REGEX_LIST:
        REGEX_LIST = [(lesson, r'\b({})\b'.format('|'.join(words))) for (lesson, words) in NEW_WORDS_PER_LESSON.items()]
        REGEX_LIST.sort(key=lambda x: x[0], reverse=True)
    for (lesson, regex) in REGEX_LIST:
        if re.search(regex, sentence):
            return lesson
    raise ValueError('No lesson found for sentence: {}'.format(sentence))
