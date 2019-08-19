#!/usr/bin/env python3

import csv
import os
import re

import translations

DEBUG_ENVVAR_KEY = 'DEBUG'
DEBUG_ENVVAR_VALUE = 'true'
DEBUG_FILE = 'translations.csv'

OFFICIAL_WORD_LIST = [
    'apeja', 'kijetesantakalu', 'kipisi', 'leko', 'monsuta', 'po', 'tuli',  # Extra/Extinct words
    'a', 'akesi', 'ala', 'alasa', 'ale', 'ali', 'anpa', 'ante', 'anu', 'awen', 'e', 'en', 'esun', 'ijo', 'ike', 'ilo',
    'insa', 'jaki', 'jan', 'jelo', 'jo', 'kala', 'kalama', 'kama', 'kasi', 'ken', 'kepeken', 'kili', 'kin', 'kiwen',
    'ko', 'kon', 'kule', 'kulupu', 'kute', 'la', 'lape', 'laso', 'lawa', 'len', 'lete', 'li', 'lili', 'linja', 'lipu',
    'loje', 'lon', 'luka', 'lukin', 'lupa', 'ma', 'mama', 'mani', 'meli', 'mi', 'mije', 'moku', 'moli', 'monsi', 'mu',
    'mun', 'musi', 'mute', 'namako', 'nanpa', 'nasa', 'nasin', 'nena', 'ni', 'nimi', 'noka', 'o', 'oko', 'olin', 'ona',
    'open', 'pakala', 'pali', 'palisa', 'pan', 'pana', 'pi', 'pilin', 'pimeja', 'pini', 'pipi', 'poka', 'poki', 'pona',
    'pu', 'sama', 'seli', 'selo', 'seme', 'sewi', 'sijelo', 'sike', 'sin', 'sina', 'sinpin', 'sitelen', 'sona',
    'soweli', 'suli', 'suno', 'supa', 'suwi', 'tan', 'taso', 'tawa', 'telo', 'tenpo', 'toki', 'tomo', 'tu', 'unpa',
    'uta', 'utala', 'walo', 'wan', 'waso', 'wawa', 'weka', 'wile']
UNOFFICIAL_WORD_REGEX = r'\b((?!(?:{}|(?:[AEIOU]|[KLMNPS][aeiou]|[JT][aeou]|W[aei])(?:(?:n?[klmps][aeiou]|n?[jt][aeou]|n?w[aei]|n[aeiou]))*n?)\b)\w+|(?:{})\b)'.format('|'.join(OFFICIAL_WORD_LIST), '|'.join(map(str.capitalize, OFFICIAL_WORD_LIST)))


def main():
    if os.environ.get('DEBUG', '').lower() == 'true':
        with open(DEBUG_FILE, newline='') as debug_csv:
            translation_rows = list(csv.reader(debug_csv, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar=''))
    else:
        translation_rows = translations.generate_translations()
    print('Finding invalid words for each row...')
    invalid_rows = sorted(
        list(filter(
            lambda mapped_row: mapped_row[1],
            map(lambda row: (row[0], sorted(re.findall(UNOFFICIAL_WORD_REGEX, row[1]))), translation_rows))),
        key=lambda x: x[1])
    print('Found {} row(s) with invalid words.'.format(len(invalid_rows)))
    for row in invalid_rows:
        print(row)
    print('Done.')


if __name__ == '__main__':
    main()
