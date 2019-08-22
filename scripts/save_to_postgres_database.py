#!/usr/bin/env python3
import csv
import flask
import os
import random
import re
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm.session import sessionmaker

import database
import invalid_sentences
import jan_pije
import translations
import words

DATABASE_ENVVAR = 'DATABASE_URL'
DATABASE_ROW_LIMIT = 10000


def main():
    if DATABASE_ENVVAR not in os.environ:
        raise KeyError('The {} envvar must be set.'.format(DATABASE_ENVVAR))
    app = flask.Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI = os.environ[DATABASE_ENVVAR],
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )
    database.db.init_app(app)
    translation_rows = translations.generate_translations()
    print('Filtering sentences with invalid words...')
    filtered_rows = list(filter(
        lambda row: not re.findall(invalid_sentences.UNOFFICIAL_WORD_REGEX, row[1]),
        translation_rows))
    print('  ... Removed {} sentences.'.format(len(translation_rows) - len(filtered_rows)))
    print('Finding lessons and extinct words for each row...')
    database_rows = list(map(lambda row: {
            'toki_pona_id': int(row[0]),
            'toki_pona_text': row[1],
            'english_id': int(row[2]),
            'english_text': row[3],
            'lesson': jan_pije.get_lesson_for_sentence(row[1]),
            'has_extinct_words': words.has_extinct_words(row[1])
        }, filtered_rows))
    final_data_chopped = len(database_rows) > DATABASE_ROW_LIMIT
    if final_data_chopped:
        random.shuffle(database_rows)
        database_rows = database_rows[:DATABASE_ROW_LIMIT]
    print('Saving to database...')
    with app.app_context():
        session = database.db.session
        table = database.Translation.__table__
        session.execute('CREATE EXTENSION IF NOT EXISTS tsm_system_rows')
        session.execute('DROP TABLE IF EXISTS %s' % table.name)
        table.create(bind=session.connection())
        session.execute(table.insert().values(database_rows))
        # session.rollback()
        session.commit()
        insert_count = database.Translation.query.count()
    print('Done. Inserted {} translations.'.format(
        '{}/{}'.format(insert_count, len(filtered_rows)) if final_data_chopped else insert_count))


if __name__ == '__main__':
    main()
