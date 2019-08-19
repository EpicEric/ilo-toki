#!/usr/bin/env python3

import csv

import translations

OUTPUT_FILE = 'translations.csv'


def main():
    translation_rows = translations.generate_translations()
    print('Writing to {}...'.format(OUTPUT_FILE))
    with open(OUTPUT_FILE, 'w', newline='') as translations_csv:
        translations_writer = csv.writer(translations_csv, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
        translations_writer.writerows(translation_rows)
    print('Done.')


if __name__ == '__main__':
    main()
