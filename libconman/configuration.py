'''
    Initializes configuration settings
    Author: Julius Pedersen <deifyed+conman@gmail.com>
'''
import configparser
import os.path

ROOT_DIR = os.path.expanduser('~/.conman')

### Creating the config
config = configparser.ConfigParser()
# Initializing default vaules
config.read_dict({
    # General settings
    'general': {
        'conman_directory': ROOT_DIR,
        'verbose': False,
    },

    # Database specific settings
    'database': {
        'path': os.path.join(ROOT_DIR, '.condb'),
    },
})
# Overwriting default values with user settings
config.read([
    os.path.expanduser('~/.config/conman'),
])

### Tools
def verbose(msg):
    if config.getboolean('general', 'verbose'):
        print(msg)
