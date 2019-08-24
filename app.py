#!/usr/bin/env python3
import flask
import flask_cors
import flask_marshmallow
import os
import threading
import time

import scripts.database as database
import scripts.jan_pije as jan_pije

DEFAULT_RANDOM_SAMPLE_SIZE = 25
MAXIMUM_RANDOM_SAMPLE_SIZE = 100


app = flask.Flask(__name__)
flask_cors.CORS(app)
app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key'),
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/ilo-toki'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)
database.db.init_app(app)
ma = flask_marshmallow.Marshmallow(app)


class TranslationSchema(ma.ModelSchema):
    class Meta:
        model = database.Translation


@app.errorhandler(404)
def not_found(error):
    error_dict = {'status': 'error', 'reason': 'Page not found'}
    return error_dict, 404


# Database healthcheck API
@app.route('/api/healthcheck', methods=['GET'])
def healthcheck():
    error_dict = {'status': 'error', 'reason': 'Unknown error'}
    try:
        database.db.engine.execute('SELECT true')
        data_dict = {'status': 'success'}
        return data_dict
    except Exception as err:
        error_dict['reason'] = 'Database is unavailable'
        return error_dict, 500


# Lessons API
@app.route('/api/lessons', methods=['GET'])
def lessons():
    data = sorted(list(jan_pije.NEW_WORDS_PER_LESSON.keys()))
    data_dict = {'status': 'success', 'data': data}
    return data_dict


# Sentences API
@app.route('/api/sentences', methods=['GET'])
def sentences():
    error_dict = {'status': 'error', 'reason': 'Unknown error'}
    # Get filter parameters (extinct_words, maximum_lesson)
    extinct_words = flask.request.args.get('extinct_words', '').lower() == 'true'
    try:
        maximum_lesson = int(flask.request.args.get('maximum_lesson', '0'))
    except ValueError:
        error_dict['reason'] = 'maximum_lesson must be a valid integer'
        return error_dict, 400
    try:
        sample_size = min(
            int(flask.request.args.get('sample_size', DEFAULT_RANDOM_SAMPLE_SIZE)),
            MAXIMUM_RANDOM_SAMPLE_SIZE)
    except ValueError:
        error_dict['reason'] = 'sample_size must be a valid integer <= {}'.format(MAXIMUM_RANDOM_SAMPLE_SIZE)
        return error_dict, 400
    # Get data from database
    query = database.Translation.query
    if not extinct_words:
        query = query.filter_by(has_extinct_words=False)
    if maximum_lesson > 0:
        query = query.filter(database.Translation.lesson <= maximum_lesson)
    rows = query.random_sample(sample_size)
    if len(rows) == 0:
        error_dict['reason'] = 'No matching data found'
        return error_dict
    data_dict = {'status': 'success', 'data': TranslationSchema().dump(rows, many=True)}
    return data_dict


if __name__ == '__main__':
    app.debug = bool(os.environ.get('DEBUG'))
    app.run()
