#!/usr/bin/env python3
import csv
import os
import re
import sys

import translations
import words

UNOFFICIAL_WORD_REGEX = r'\b((?!(?:{}|(?:[AEIOU]|[KLMNPS][aeiou]|[JT][aeou]|W[aei])(?:(?:n?[klmps][aeiou]|n?[jt][aeou]|n?w[aei]|n[aeiou]))*n?)\b)\w+|(?:{})\b)'.format('|'.join(words.FULL_WORD_LIST), '|'.join(map(str.capitalize, words.FULL_WORD_LIST)))


def main():
    translation_rows = translations.generate_translations()
    print('Finding invalid words for each row...')
    invalid_rows = sorted(
        list(filter(
            lambda mapped_row: mapped_row[1],
            map(lambda row: (row[0], sorted(re.findall(UNOFFICIAL_WORD_REGEX, row[1]))), translation_rows))),
        key=lambda x: x[1])
    print('Found {} row(s) with invalid words.'.format(len(invalid_rows)))
    for row in invalid_rows:
        print(row, file=sys.stderr)
    print('Done.')


if __name__ == '__main__':
    main()
