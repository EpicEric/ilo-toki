#!/usr/bin/env python3
import csv
import os
import psycopg2
import psycopg2.extras
import random
import re

import invalid_sentences
import jan_pije
import translations
import words

DATABASE_ENVVAR = 'DATABASE_URL'
DATABASE_ROW_LIMIT = 10000


def main():
    if DATABASE_ENVVAR not in os.environ:
        raise KeyError('The {} envvar must be set.'.format(DATABASE_ENVVAR))
    database_url = os.environ[DATABASE_ENVVAR]
    translation_rows = translations.generate_translations()
    print('Filtering sentences with invalid words...')
    filtered_rows = list(filter(
        lambda row: not re.findall(invalid_sentences.UNOFFICIAL_WORD_REGEX, row[1]),
        translation_rows))
    print('  ... Removed {} sentences.'.format(len(translation_rows) - len(filtered_rows)))
    print('Finding lessons and extinct words for each row...')
    database_rows = list(map(lambda row: (
            row[0], row[1], row[2], row[3], jan_pije.get_lesson_for_sentence(row[1]), words.has_extinct_words(row[1])
        ), filtered_rows))
    final_data_chopped = len(database_rows) > DATABASE_ROW_LIMIT
    if final_data_chopped:
        random.shuffle(database_rows)
        database_rows = database_rows[:DATABASE_ROW_LIMIT]
    print('Saving to database...')
    # TODO: Use SQLAlchemy from Flask app to avoid data inconsistencies
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as curs:
            curs.execute('CREATE EXTENSION IF NOT EXISTS tsm_system_rows;')
            curs.execute('DROP TABLE IF EXISTS translations;')
            curs.execute("""
                CREATE TABLE translations (
                    id SERIAL NOT NULL PRIMARY KEY,
                    toki_pona_id INTEGER UNIQUE NOT NULL,
                    toki_pona_text TEXT NOT NULL,
                    english_id INTEGER UNIQUE NOT NULL,
                    english_text TEXT NOT NULL,
                    lesson INTEGER NOT NULL,
                    has_extinct_words BOOLEAN NOT NULL
                );""")
            psycopg2.extras.execute_values(curs, """
                    INSERT INTO translations
                        (toki_pona_id, toki_pona_text, english_id, english_text, lesson, has_extinct_words)
                    VALUES %s;""",
                database_rows)
    print('Done. Inserted {} translations.'.format(
        '{}/{}'.format(DATABASE_ROW_LIMIT, len(filtered_rows)) if final_data_chopped else len(database_rows)))


if __name__ == '__main__':
    main()
