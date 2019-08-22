# scripts / ilo pali

Any necessary/useful scripts that aren't a part of the main web application.

## `create_translations_file.py`

Saves Tatoeba data to `translations.csv`. It can then be used by other commands -- see `translations.py` in "Other files".

## `save_to_postgres_database.py`

Stores translation data to a PostgreSQL database, including the respective jan Pije lesson and if it contains extinct words.

Sentences with invalid words are filtered out. The number of sentences inserted in the database is also limited to 10000 rows because of [Heroku's free plan limitations](https://elements.heroku.com/addons/heroku-postgresql).

## `invalid_sentences.py`

Prints list of Tatoeba sentences IDs with invalid words to stderr. To export them to a file:

```sh
./scripts/invalid_sentences.py 2> /path/to/file.txt
```

## Other files / lipu ante

- `database.py` - Full database configuration with SQLAlchemy.
- `translations.py` - Handles downloading, filtering and generating translation data from Tatoeba. For debugging with an existing `translation.csv` file in the current directory instead of fetching content remotely, set the envvar `DEBUG=true`.
- `jan_pije.py` - Finds the respective [jan Pije lesson](http://tokipona.net/tp/janpije/okamasona.php) for a given sentence.
- `words.py` - List of all non-borrowed words in Toki Pona, whether official or extinct/extra.
