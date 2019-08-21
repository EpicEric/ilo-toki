import collections
import csv
import os
import tarfile
import tempfile
import urllib.request


SENTENCES_CSV = 'sentences.csv'
SENTENCES_URL = 'https://downloads.tatoeba.org/exports/sentences.tar.bz2'
LINKS_CSV = 'links.csv'
LINKS_URL = 'https://downloads.tatoeba.org/exports/links.tar.bz2'

SEEK_CACHE_CHUNK = 1000

DEBUG_ENVVAR_KEY = 'DEBUG'
DEBUG_ENVVAR_VALUE = 'true'
DEBUG_FILE = 'translations.csv'


class LastUpdatedOrderedDict(collections.OrderedDict):
        """Store items in the order the keys were last added."""

        def __setitem__(self, key, value):
            if key in self:
                del self[key]
            collections.OrderedDict.__setitem__(self, key, value)


def generate_translations():
    if os.environ.get(DEBUG_ENVVAR_KEY, '').lower() == DEBUG_ENVVAR_VALUE.lower():
        if os.path.isfile(DEBUG_FILE):
            print('Loading debug data from translations file "{}"...'.format(DEBUG_FILE))
            with open(DEBUG_FILE, newline='') as debug_csv:
                return list(csv.reader(debug_csv, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar=''))
        else:
            raise OSError('Missing debug translations file {}'.format(DEBUG_FILE))

    with tempfile.TemporaryDirectory() as tempdir:

        print('Fetching "{}" from Tatoeba.org...'.format(SENTENCES_CSV))
        with urllib.request.urlopen(SENTENCES_URL) as response:
            if response.getcode() != 200:
                raise ValueError('Request returned invalid HTTP code {}'.format(response.getcode()))
            with tarfile.open(mode='r|bz2', fileobj=response) as archive:
                archive.extractall(path=tempdir)
        sentences_file = os.path.join(tempdir, SENTENCES_CSV)

        print('Fetching "{}" from Tatoeba.org...'.format(LINKS_CSV))
        with urllib.request.urlopen(LINKS_URL) as response:
            if response.getcode() != 200:
                raise ValueError('Request returned invalid HTTP code {}'.format(response.getcode()))
            with tarfile.open(mode='r|bz2', fileobj=response) as archive:
                archive.extractall(path=tempdir)
        links_file = os.path.join(tempdir, LINKS_CSV)

        seek_cache = {0: 0}
        print('Generating seek cache with chunk size of {}...'.format(SEEK_CACHE_CHUNK))
        with open(sentences_file, newline='') as cache_file:
            tell = cache_file.tell()
            line = cache_file.readline()
            index = 0
            index_pos = 0
            while line:
                new_index = int(line.split('\t')[0])
                new_index_pos = new_index % SEEK_CACHE_CHUNK
                if new_index_pos == 0 or new_index_pos < index_pos:
                    seek_cache[new_index // SEEK_CACHE_CHUNK] = tell
                index = new_index
                index_pos = new_index_pos
                if SEEK_CACHE_CHUNK - index_pos < 20: # If getting close to end of chunk, keep updating tell
                    tell = cache_file.tell()
                line = cache_file.readline()
        print('  ... Created {} cache keys.'.format(len(seek_cache)))

        TRANSLATIONS_DICT = LastUpdatedOrderedDict()
        print('Generating translations...')
        with \
                open(sentences_file, newline='') as toki_pona_csv, \
                open(links_file, newline='') as links_csv, \
                open(sentences_file, newline='') as english_csv:
            toki_pona_reader = csv.reader(toki_pona_csv, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
            links_reader = csv.reader(links_csv, delimiter='\t')
            english_reader = csv.reader(english_csv, delimiter='\t', quoting=csv.QUOTE_NONE, quotechar='')
            links_row = next(links_reader)
            # For every toki pona sentence
            for tp_row in (row for row in toki_pona_reader if row[1] == 'toki'):
                try:
                    # Find first link for the current toki pona sentence
                    while int(links_row[0]) < int(tp_row[0]):
                        links_row = next(links_reader)
                    # Check every link for the current toki pona sentence
                    while int(links_row[0]) == int(tp_row[0]):
                        # Position seek in file with seek cache
                        seek_cache_index = int(links_row[1]) // SEEK_CACHE_CHUNK
                        while True:
                            # Handle index possibly missing in seek cache
                            try:
                                english_csv.seek(seek_cache[seek_cache_index])
                                break
                            except KeyError:
                                if seek_cache_index == 0:
                                    raise
                                seek_cache_index -= 1
                        # Get corresponding linked row
                        eng_row = next(english_reader)
                        # Skip rows while we haven't reached the intended link
                        while int(eng_row[0]) < int(links_row[1]):
                            eng_row = next(english_reader)
                        # Check if linked row is in English
                        if int(eng_row[0]) == int(links_row[1]) and eng_row[1] == 'eng':
                            # Write Toki Pona sentence and its translation to a dict, so that there's only one toki pona
                            # sentence per English sentence
                            TRANSLATIONS_DICT[int(eng_row[0])] = (int(tp_row[0]), tp_row[2], int(eng_row[0]), eng_row[2])
                            break
                        # Linked row is not in English; try next link
                        links_row = next(links_reader)
                except StopIteration:
                    break
        print('  ... Created {} translations.'.format(len(TRANSLATIONS_DICT)))
        return TRANSLATIONS_DICT.values()
