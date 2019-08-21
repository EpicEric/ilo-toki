#!/usr/bin/env python3
import flask
import flask_cors
import flask_sqlalchemy
import os
import threading
import time


# Random sampling with PostgreSQL extension tsm_system_rows
class TablesampleQuery(flask_sqlalchemy.BaseQuery):
    def random_sample(n):
        return self.suffix_with('TABLESAMPLE SYSTEM_ROWS(%d)' % n).all()


app = flask.Flask(__name__)
flask_cors.CORS(app)
app.config.from_mapping(
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev_key'),
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://localhost/ilo-toki'),
    SQLALCHEMY_TRACK_MODIFICATIONS = False
)
db = flask_sqlalchemy.SQLAlchemy(app, query_class=TablesampleQuery)


# Translation model
class Translation(db.Model):
    __tablename__ = 'translations'

    toki_pona_id = db.Column(db.Integer, unique=True, nullable=False)
    toki_pona_text = db.Column(db.Text, nullable=False)
    english_id = db.Column(db.Integer, unique=True, nullable=False)
    english_text db.Column(db.Text, nullable=False)
    lesson = db.Column(db.Integer, nullable=False)
    has_extinct_words = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Translation toki({})=eng({})>'.format(self.toki_pona_id, self.english_id)


# Sentences API
@app.route('/sentences', methods=['GET'])
def sentences():
    error_dict = {'status': 'error', 'reason': 'Unknown error'}
    # TODO: Get data from database
    error_dict['reason'] = 'Unimplemented endpoint'
    return flask.jsonify(error_dict)


# Serve front-end
@app.route('/', methods=['GET'])
def enigma():
    error_dict = {'status': 'error', 'reason': 'Unknown error'}
    # TODO: Serve frontend
    error_dict['reason'] = 'Unimplemented endpoint'
    return flask.jsonify(error_dict)


if __name__ == '__main__':
    app.debug = bool(os.environ.get('DEBUG_MODE'))
    app.run()
