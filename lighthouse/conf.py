import yaml
import os
import base64
from lbrynet.core.utils import generate_id


def get_settings(path):
    f = open(path, "r")
    decoded_settings = yaml.load(f.read())
    f.close()
    return decoded_settings


def save_settings(path, settings):
    f = open(path, "w")
    f.write(yaml.dump(settings))
    f.close()


conf = os.path.join(os.path.expanduser("~"), ".lighthouse.yml")
default_settings = {
    'cache dir': os.path.join(os.path.expanduser("~"), '.lighthouse'),
    'default search keys': ['title', 'description', 'author', 'name'],
    'weights': {'name': 1.25, 'title': 1.0, 'description': 1.0, 'author': 1.0},
    'max returned results': 25,
    'cache size': 1000,
    'max results cached': 25,
    'max sd attempts': 1,
    'filtered uris': ['socialengineering'],
    'lbryid': base64.encodestring(generate_id()),
    'reflector_port': 5567,
    'txindex': False,
    'verbose lbrycrdd': False
}

if not os.path.isfile(conf):
    save_settings(conf, default_settings)

settings = get_settings(conf)

for setting in default_settings:
    if setting not in settings:
        settings[setting] = default_settings[setting]

save_settings(conf, settings)

CACHE_DIR = settings['cache dir']
DEFAULT_SEARCH_KEYS = settings['default search keys']
METADATA_INDEXES = ['title', 'description', 'author']
DEFAULT_SETTINGS = {'search_by': DEFAULT_SEARCH_KEYS}
DEFAULT_WEIGHTS = settings['weights']
MAX_RETURNED_RESULTS = settings['max returned results']
CACHE_SIZE = settings['cache size']
MAX_SD_TRIES = settings['max sd attempts']
MAX_RESULTS_CACHED = settings['max results cached']
FILTERED = settings['filtered uris']
LBRYID = settings['lbryid']
REFLECTOR_PORT = settings['reflector_port']
USE_TXINDEX = settings['txindex']
VERBOSE_LBRYCRDD = settings['verbose lbrycrdd']

if not os.path.isdir(CACHE_DIR):
    os.mkdir(CACHE_DIR)
