import flask_sqlalchemy
from sqlalchemy.sql.expression import func
import random


# Random sampling with PostgreSQL extension tsm_system_rows
# TODO: See if this needs improvement?
class TablesampleQuery(flask_sqlalchemy.BaseQuery):
    def random_sample(self, n):
        return self.order_by(func.random()).limit(n).all()


db = flask_sqlalchemy.SQLAlchemy(query_class=TablesampleQuery)


# Translation model for the database
class Translation(db.Model):
    __tablename__ = 'translations'

    id = db.Column(db.Integer, primary_key=True)
    toki_pona_id = db.Column(db.Integer, unique=True, nullable=False)
    toki_pona_text = db.Column(db.Text, nullable=False)
    english_id = db.Column(db.Integer, unique=True, nullable=False)
    english_text = db.Column(db.Text, nullable=False)
    lesson = db.Column(db.Integer, nullable=False)
    has_extinct_words = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return '<Translation toki({})=eng({})>'.format(self.toki_pona_id, self.english_id)
