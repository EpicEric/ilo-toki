# ilo toki

Simple web application and API to learn Toki Pona from a corpus of sentences and their English translations.

## Features / ijo lon

All of the following features are currently WIP. They are integrated into the persistence scripts and API, but are not yet available through a front-end.

- Filter by [jan Pije's lessons](http://tokipona.net/tp/janpije/okamasona.php) if you are learning along.
- Choose between translating Toki Pona <-> English or the other way around.
- Found an error? Improve the original sentences on Tatoeba.

## Status / tenpo lon

| Service | Status |
|---------|--------|
| API | ![API badge](https://heroku-badge.herokuapp.com/?app=ilo-toki&root=api/healthcheck) |
| Database script | [![Database script badge](https://circleci.com/gh/EpicEric/ilo-toki.svg?style=svg)](https://circleci.com/gh/EpicEric/ilo-toki) |
| Frontend | ![Frontend badge](https://img.shields.io/badge/-WIP-inactive)

## Project structure / sijelo ilo

The Python 3 scripts need a few libraries available from `requirements.txt`. The recommended way to install these is with a [virtualenv](https://virtualenv.pypa.io/). After setting it up, run:

```bash
pip install -r requirements.txt
```

The project is structured as follows:

- `app.py`: Main Flask application.
- `scripts/`: Database definitions and auxiliary scripts, such as scripts to download translations and insert to PostgreSQL. See the [README](scripts/README.md) for more information.
- `Procfile` and `app.json`: Heroku's application and manifest files, respectively.
- `.circleci`: CircleCI script to re-populate database every week.

## Attributions / jo pi jan ante

The application and PostgreSQL database are hosted in Heroku under their free plans.

The [translation files](https://tatoeba.org/eng/downloads) are provided by Tatoeba under CC BY 2.0 FR.
