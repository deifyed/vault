import configparser
import os.path

CONFIG_PATHS = [
    os.path.expanduser('~/.config/conman'),
]

ROOT_DIR = os.path.expanduser('~/.conman')

_DEFAULTS = {
    # General settings
    'general': {
        'conman_directory': ROOT_DIR,
    },

    # Database specific settings
    'database': {
        'path': os.path.join(ROOT_DIR, '.condb'),
    }
}

def initConfig():
    config = configparser.ConfigParser()

    config.read_dict(_DEFAULTS)
    config.read(CONFIG_PATHS)

    return config

config = initConfig()
