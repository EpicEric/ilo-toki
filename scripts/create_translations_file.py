#!/usr/bin/env python3
import csv
import os

import translations


def main():
    if os.environ.get(translations.DEBUG_ENVVAR_KEY, '').lower() == translations.DEBUG_ENVVAR_VALUE.lower():
        raise OSError('Cannot accept envvar {}={} when creating translations file'.format(
            translations.DEBUG_ENVVAR_KEY, translations.DEBUG_ENVVAR_VALUE))
    translation_rows = translations.generate_translations()
    print('Writing to {}...'.format(translations.DEBUG_FILE))
    with open(translations.DEBUG_FILE, 'w', newline='') as translations_csv:
        translations_writer = csv.writer(translations_csv, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
        translations_writer.writerows(translation_rows)
    print('Done.')


if __name__ == '__main__':
    main()
