#!/usr/bin/env python3

import os
import psycopg2
import psycopg2.extras
import random

import jan_pije
import translations

DATABASE_ENVVAR = 'DATABASE_URL'
DATABASE_ROW_LIMIT = 10000


def main():
    if DATABASE_ENVVAR not in os.environ:
        raise KeyError('The {} envvar must be set.'.format(DATABASE_ENVVAR))
    database_url = os.environ[DATABASE_ENVVAR]
    translation_rows = translations.generate_translations()
    print('Finding lesson for each row...')
    database_rows = list(
        map(lambda row: (row[0], row[1], row[2], row[3], jan_pije.get_lesson_for_sentence(row[1])), translation_rows))
    if len(database_rows) > DATABASE_ROW_LIMIT:
        random.shuffle(database_rows)
        database_rows = database_rows[:DATABASE_ROW_LIMIT]
    print('Saving to database...')
    with psycopg2.connect(database_url) as conn:
        with conn.cursor() as curs:
            curs.execute('CREATE EXTENSION IF NOT EXISTS tsm_system_rows;')
            curs.execute("""
                CREATE TABLE IF NOT EXISTS translations (
                    toki_pona_id INTEGER UNIQUE NOT NULL,
                    toki_pona_text TEXT NOT NULL,
                    english_id INTEGER UNIQUE NOT NULL,
                    english_text TEXT NOT NULL,
                    lesson INTEGER NOT NULL
                );""")
            curs.execute('DELETE FROM translations;')
            psycopg2.extras.execute_values(curs, """
                    INSERT INTO translations (toki_pona_id, toki_pona_text, english_id, english_text, lesson)
                    VALUES %s;""",
                database_rows)
    print('Done.')


if __name__ == '__main__':
    main()
